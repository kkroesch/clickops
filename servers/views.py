from django.shortcuts import render

from rest_framework import viewsets
from .models import Network, Server
from .serializers import NetworkSerializer, ServerSerializer

class NetworkViewSet(viewsets.ModelViewSet):
    queryset = Network.objects.all()
    serializer_class = NetworkSerializer

class ServerViewSet(viewsets.ModelViewSet):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer