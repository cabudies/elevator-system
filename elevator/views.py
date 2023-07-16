from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework import status

from . import models
from . import serializers


class ElevatorSystemViewSet(ModelViewSet):
    queryset = models.ElevatorSystem.objects.all()
    serializer_class = serializers.ElevatorSystemSerializer
    permission_classes = (AllowAny,)
    
    def list(self, request):
        serializer = serializers.ElevatorSystemSerializer(self.queryset, many=True)
        print("serializer list=======")
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        item = get_object_or_404(self.queryset, pk=pk)
        serializer = serializers.ElevatorSystemSerializer(item)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            serializer.data, 
            status=status.HTTP_201_CREATED
        )
    