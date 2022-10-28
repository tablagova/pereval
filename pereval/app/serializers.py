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

        def create(self, validated_data):
            return Users.objects.create(**validated_data)

        def update(self, instance, validated_data):
            instance.phone = validated_data.get('phone', instance.phone)
            instance.fam = validated_data.get('fam', instance.fam)
            instance.name = validated_data.get('name', instance.name)
            instance.otc = validated_data.get('otc', instance.otc)
            instance.save()
            return instance


class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = [
            'id',
            'latitude',
            'longitude',
            'height'
        ]

        def create(self, validated_data):
            return Coords.objects.create(**validated_data)


class PerevalAddedSerializer(serializers.ModelSerializer):

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

        def create(self, validated_data):
            return PerevalAdded.objects.create(**validated_data)


class ImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Images
        fields = [
            'id',
            'date_added',
            'title',
            'img',
            'pereval',
        ]

        def create(self, validated_data):
            return Images.objects.create(**validated_data)
