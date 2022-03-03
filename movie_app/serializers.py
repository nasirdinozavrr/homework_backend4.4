from rest_framework import serializers
from movie_app.models import Director, Movie, Review
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = 'id name count_movies'.split()


class DirectorCreateUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=6, max_length=10)




class MovieSerializer(serializers.ModelSerializer):
    director = DirectorSerializer()

    class Meta:
        model = Movie
        fields = 'id title duration description director rating'.split()


class MovieCreateUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=2, max_length=50)
    description = serializers.CharField()
    duration = serializers.CharField(max_length=50)
    director_id = serializers.IntegerField()

    def validate_director_id(self, director_id):
        if Director.objects.filter(id=director_id).count()==0:
            raise ValidationError(f'Movie with id={director_id} not found!')
        return director_id




class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'id text stars'.split()

class ReviewCreateUpdateSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=10, min_length=5)
    stars = serializers.IntegerField(min_value=1, max_value=5)


class UserCreateSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate_username(self, username):
        if User.objects.filter(username=username):
            raise ValueError('User with this username already exist!')
        return username


class AuthorizationSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
