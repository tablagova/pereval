from django.shortcuts import render
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from app.serializers import *


class PerevalAPIView(APIView):

    def post(self, request):
        data = request.data
        email = data['user']['email']
        if Users.objects.filter(email=email).exists():
            user = Users.objects.get(email=email)
        else:
            user_serializer = UsersSerializer(data=data['user'])
            if user_serializer.is_valid():
                user = user_serializer.save()
            else:
                return Response({'message': user_serializer.errors, 'id': None}, status=400)

        coords_serializer = CoordsSerializer(data=data['coords'])
        if coords_serializer.is_valid():
            coords_new = coords_serializer.save()
        else:
            return Response({'message': coords_serializer.errors, 'id': None}, status=400)


        data['user'] = user.id
        data['coord'] = coords_new.id
        data['winter_level'] = data['level']['winter']
        data['summer_level'] = data['level']['summer']
        data['autumn_level'] = data['level']['autumn']
        data['spring_level'] = data['level']['spring']

        serializer = PerevalAddedSerializer(data=data)
        if serializer.is_valid():
            pereval_new = serializer.save()
        else:
            return Response({'message': serializer.errors, 'id': None}, status=400)

        images = data['images']
        for image in images:
            image['pereval'] = pereval_new.id
            image_serializer = ImagesSerializer(data=image)
            if image_serializer.is_valid():
                image_serializer.save()
            else:
                return Response({'message': image_serializer.errors, 'id': None}, status=400)

        return Response({'message': None, 'id': pereval_new.id}, status=200)
