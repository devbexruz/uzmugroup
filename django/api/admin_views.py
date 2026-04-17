from django.contrib import admin
from ..pages.models import *
from .admin_serializers import *
from rest_framework import generics





class AdminCreateUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
