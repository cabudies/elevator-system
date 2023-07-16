from rest_framework import serializers

from . import models

class ElevatorSystemSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ElevatorSystem
        fields = '__all__'


class ElevatorSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Elevator
        fields = '__all__'


class ElevatorRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ElevatorRequest
        fields = '__all__'

