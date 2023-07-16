from rest_framework import serializers

from . import models

class ElevatorSystemSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ElevatorSystem
        fields = '__all__'

