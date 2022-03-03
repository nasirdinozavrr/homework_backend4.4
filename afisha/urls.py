from django.contrib import admin
from django.urls import path, include
from movie_app import views

urlpatterns = [
    path('api/v1/directors/', views.DirectorCreateUpdateAPIView.as_view()),
    path('api/v1/directors/<int:id>/', views.DirectorUpdateDeleteAPIView.as_view()),
    path('api/v1/movies/', views.MovieCreateUpdateAPIView.as_view()),
    path('api/v1/movies/<int:id>/', views.MovieUpdateDeleteAPIView.as_view()),
    path('api/v1/reviews/', views.ReviewCreateUpdateAPIView.as_view()),
    path('api/v1/reviews/<int:id>/', views.ReviewUpdateDeleteAPIView.as_view()),
    path('api/v1/registration/', views.RegisterAPIView.as_view()),
    path('api/v1/login/', views.AuthorizationAPIView.as_view()),
    ]