from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from .serializers import *
from .models import PerevalAdded, ADDED_STATUS
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class PerevalAPIView(viewsets.ViewSet):

    def serializer_error_response(self, errors, param='id'):
        message = ''
        for k, v in errors.items():
            message += f'{k}: {str(*v)}'
        if param == 'state':
            return Response({'message': message, 'state': 0}, status=400)
        else:
            return Response({'message': message, 'id': None}, status=400)

    def get_one(self, request, **kwargs):
        try:
            pereval = PerevalAdded.objects.get(pk=kwargs['pk'])
            data = PerevalAddedSerializer(pereval).data
            return Response(data, status=200)
        except:
            return Response({'message': "There's no such record", 'id': None}, status=400)

    user_email = openapi.Parameter('user_email', openapi.IN_QUERY, description="user e-mail", type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[user_email])
    def get_user_records(self, request, **kwargs):
        try:
            user = Users.objects.get(email=request.GET['user_email'])
            perevals = PerevalAdded.objects.filter(user=user)
        except:
            perevals = {}
        data = PerevalAddedSerializer(perevals, many=True).data
        return Response(data, status=200)

    @swagger_auto_schema(request_body=PerevalAddedSerializer)
    def post(self, request):
        try:
            data = request.data

            def create_dependence(serializer):
                if serializer.is_valid():
                    return serializer.save()
                else:
                    return self.serializer_error_response(serializer.errors)

            try:
                user = Users.objects.get(email=data['user']['email'])
                user_serializer = UsersSerializer(user, data=data['user'])
            except:
                user_serializer = UsersSerializer(data=data['user'])

            try:
                images = data['images']
                data.pop('images')
            except:
                images = []

            serializer = PerevalAddedSerializer(data=data)
            if serializer.is_valid():
                data.pop('user')
                pereval_new = PerevalAdded.objects.create(
                    user=create_dependence(user_serializer),
                    coords=create_dependence(CoordsSerializer(data=data.pop('coords'))),
                    level=create_dependence(LevelSerializer(data=data.pop('level'))),
                    **data)
            else:
                return self.serializer_error_response(serializer.errors)

            for image in images:
                image['pereval'] = pereval_new.id
                create_dependence(ImagesSerializer(data=image))

            return Response({'message': None, 'id': pereval_new.id}, status=201)

        except Exception as inst:
            return Response({'message': str(inst), 'id': None}, status=500)

    @swagger_auto_schema(metods=['patch'], request_body=PerevalAddedSerializer)
    def edit_one_record(self, reguest, **kwargs):
        try:
            pereval = PerevalAdded.objects.get(pk=kwargs['pk'])
            if pereval.status == 'new':
                data = reguest.data
                data.pop('user')
                Images.objects.filter(pereval_id=pereval.id).delete()
                images = data.pop('images')
                serializers = []
                serializers.append(CoordsSerializer(Coords.objects.get(id=pereval.coords_id), data=data.pop('coords')))
                serializers.append(LevelSerializer(Level.objects.get(id=pereval.level_id), data=data.pop('level')))
                serializers.append((PerevalAddedSerializer(pereval, data=data)))
                for image in images:
                    image['pereval'] = pereval.id
                    serializers.append(ImagesSerializer(data=image))
                for serializer in serializers:
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        return self.serializer_error_response(serializer.errors, 'state')
                return Response({'message': None, 'state': 1}, status=202)
            else:
                return Response({'message': "The status of record isn't new", 'state': 0}, status=400)
        except:
            return Response({'message': "There's no such record", 'state': 0}, status=400)
