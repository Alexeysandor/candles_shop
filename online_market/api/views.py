from django.shortcuts import render
from djoser.views import UserViewSet
from api.serializers import UserCreateSerializer
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

