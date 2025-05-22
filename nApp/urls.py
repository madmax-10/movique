from django.contrib import admin
from django.urls import path
from nApp import views

urlpatterns = [
    path("", views.index.as_view(), name='home'),
    path("signin/",views.signin, name='signIn'),
    path("signup/",views.signup, name='signUp'),
    path("logout/",views.logout, name='logOut'),
    path("create/",views.create.as_view(),name='vidCreate'),
    path("<int:pk>/",views.detail.as_view(),name='video-detail'),
    path("<str:filter>/<str:text>",views.vidList.as_view(),name='videos'),
    # path("register/",views.register, name='register'),
    # path("login/",views.login, name='login'),
]


