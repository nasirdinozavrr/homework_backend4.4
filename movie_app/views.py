from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from movie_app.serializers import DirectorSerializer, MovieSerializer, ReviewSerializer
from movie_app.serializers import DirectorCreateUpdateSerializer, MovieCreateUpdateSerializer, ReviewCreateUpdateSerializer
from movie_app.models import Director, Movie, Review
from rest_framework import status
from movie_app import serializers
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
@api_view(["GET", "POST"])
def director_list_view(request):
    if request.method == "GET":
        directors = Director.objects.all()
        data = DirectorSerializer(directors, many=True).data
        return Response(data=data)
    elif request.method == "POST":
        serializer = DirectorCreateUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data={'errors': serializer.errors},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        print(request.data)
        name = request.data.get('name')
        director = Director.objects.create(name=name)
        return Response(data=DirectorSerializer(director).data, status=status.HTTP_201_CREATED)

@api_view(["GET", "PUT", "DELETE"])
def director_detail_view(request, id):
    try:
        director = Director.objects.get(id=id)
    except Director.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'message': 'Director not found'})
    if request.method == "GET":
        data = DirectorSerializer(director).data
        return Response(data=data)
    elif request.method == "DELETE":
        director.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == "PUT":
        serializer = DirectorCreateUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
                            data={'errors': serializer.errors})
        director.name = request.data.get('name')
        director.save()
        return Response(data=DirectorSerializer(director).data)




@api_view(["GET", "POST"])
def movie_list_view(request):
    if request.method == "GET":
        movies = Movie.objects.all()
        data = MovieSerializer(movies, many=True).data
        return Response(data=data)
    elif request.method == "POST":
        serializer = MovieCreateUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
                            data={'errors': serializer.errors})
        print(request.data)
        title = request.data.get('title')
        description = request.data.get('description')
        director_id = request.data.get('director_id')
        movie = Movie.objects.create(title=title, description=description, director_id=director_id)
        return Response(data=MovieSerializer(movie).data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "DELETE"])
def movie_detail_view(request, id):
    try:
        movie = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'message': 'Movie not found'})
    if request.method == "GET":
        data = MovieSerializer(movie).data
        return Response(data=data)
    elif request.method == "DELETE":
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == "PUT":
        serializer = MovieCreateUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
                            data={'errors': serializer.errors})
        movie.title = request.data.get('title')
        movie.description = request.data.get('description')
        movie.duration = request.data.get('duration')
        movie.director_id = request.data.get('director_id')
        movie.save()
        return Response(data=MovieSerializer(movie).data)




@api_view(["GET", "POST"])
def review_list_view(request):
    if request.method == "GET":
        reviews = Review.objects.all()
        data = ReviewSerializer(reviews, many=True).data
        return Response(data=data)
    elif request.method == "POST":
        serializer = serializers.ReviewCreateUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
                            data={'errors': serializer.errors})
        print(request.data)
        text = request.data.get('text')
        stars = request.data.get('stars')
        movies_id = request.data.get('movies_id')
        review = Review.objects.create(text=text, stars=stars, movies_id=movies_id)
        return Response(data=ReviewSerializer(review).data, status=status.HTTP_201_CREATED)

@api_view(["GET", "PUT", "DELETE"])
def review_detail_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'message': 'Review not found'})
    if request.method == "GET":
        data = ReviewSerializer(review).data
        return Response(data=data)
    elif request.method == "DELETE":
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == "PUT":
        serializer = ReviewCreateUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
                            data={'errors': serializer.errors})
        review.text = request.data.get('text')
        review.stars = request.data.get('stars')
        review.movies_id = request.data.get('movies_id')
        review.save()
        return Response(data=ReviewSerializer(review).data)
@api_view(['POST'])
def authorization(request):
    if request.method == "POST":
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            try:
                token = Token.objects.get(user=user)
            except Token.DoesNotExist:
                token = Token.objects.create(user=user)
            return Response(data={'key': token.key})
        return Response(data={'error': 'User not found'},
                        status=status.HTTP_404_NOT_FOUND)

@api_view(["POST"])
def registration(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        User.objects.create_user(username=username, password=password)
        return Response(data={'massage': 'User created'},
                        status=status.HTTP_201_CREATED)