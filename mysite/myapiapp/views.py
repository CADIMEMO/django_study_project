from django.shortcuts import render
from django.contrib.auth.models import Group
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework.mixins import ListModelMixin
from .serializers import GroupSerializer
# Create your views here.

@api_view()
def hello_world_view(request: Request):
    return Response({'message': 'Hello world!'})


class GroupListView(ListCreateAPIView):

    queryset = Group.objects.all()
    serializer_class = GroupSerializer

