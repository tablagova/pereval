from .models import *
from rest_framework import serializers


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = [
            'id',
            'email',
            'phone',
            'fam',
            'name',
            'otc',
        ]


class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = [
            'id',
            'latitude',
            'longitude',
            'height'
        ]


class PerevalAddedSerializer(serializers.ModelSerializer):
    coord = CoordsSerializer(read_only=True)
    # image = ImagesSerializer(read_only=True)
    user = UsersSerializer(read_only=True)

    class Meta:
        model = PerevalAdded
        fields = [
            'id',
            'date_added',
            'beauty_title',
            'title',
            'other_titles',
            'connect',
            'add_time',
            'user',
            'coord',
            'winter_level',
            'summer_level',
            'autumn_level',
            'spring_level',
            'status',
        ]


class ImagesSerializer(serializers.ModelSerializer):
    pereval = PerevalAddedSerializer(read_only=True)

    class Meta:
        model = Images
        fields = [
            'id',
            'date_added',
            'title',
            'img',
        ]
