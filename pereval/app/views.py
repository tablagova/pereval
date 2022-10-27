from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from app.models import *
from app.serializers import *

class PerevalAPIView(APIView):
    def post(self, request):
        data = request.data
        serializer = PerevalAddedSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        user = data['user']
        if Users.objects.filter(email=user['email']).exists():
            user_new = Users.objects.get(email=user['email'])
        else:
            user_new = Users.objects.create(
                email=user['email'],
                phone=user['phone'],
                fam=user['fam'],
                name=user['name'],
                otc=user['otc']
            )

        coords = data['coords']
        coords_new = Coords.objects.create(
            latitude=coords['latitude'],
            longitude=coords['longitude'],
            height=coords['height']
        )

        pereval_new = PerevalAdded.objects.create(
            beauty_title=data['beauty_title'],
            title=data['title'],
            other_titles=data['other_titles'],
            connect=data['connect'],
            add_time=data['add_time'],
            user=user_new,
            coord=coords_new,
            winter_level=data['level']['winter'],
            summer_level=data['level']['summer'],
            autumn_level=data['level']['autumn'],
            spring_level=data['level']['spring']
        )

        images = data['images']
        for image in images:
            Images.objects.create(
                title=image['title'],
                # img=image['data'],
                pereval=pereval_new
            )

        data_new = PerevalAddedSerializer(pereval_new).data
        data_new['images'] = list(pereval_new.images_set.all().values('title'))
        return Response({'post': data_new}, status=200)
