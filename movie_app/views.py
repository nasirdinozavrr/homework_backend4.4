from rest_framework.response import Response
from movie_app.serializers import DirectorSerializer, MovieSerializer, ReviewSerializer
from movie_app.models import Director, Movie, Review
from movie_app import serializers, models
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.models import User
from rest_framework import status
from .serializers import UserCreateSerializer


class DirectorCreateUpdateAPIView(ListCreateAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    pagination_class = PageNumberPagination
    filter_fields = ['name']

class DirectorUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    lookup_field = 'id'


class MovieCreateUpdateAPIView(ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    pagination_class = PageNumberPagination
    filter_fields = ['title']

class MovieUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    lookup_field = 'id'


class ReviewCreateUpdateAPIView(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination

class ReviewUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = 'id'


class AuthorizationAPIView(GenericAPIView):
    serializer_class = serializers.AuthorizationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(**serializer.validated_data)
        if user:
            try:
                token = Token.objects.get(user=user)
            except Token.DoesNotExist:
                token = Token.objects.create(user=user)
            return Response(data={'key': token.key})
        return Response(data={'error': 'User not found!'}, status=status.HTTP_404_NOT_FOUND)


class RegisterAPIView(GenericAPIView):
    serializer_class = UserCreateSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        User.objects.create_user(**serializer.validated_data)
        return Response(data={'message': 'User created'},
                        status=status.HTTP_201_CREATED)