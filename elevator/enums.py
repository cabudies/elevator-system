from django.db import models

class ElevatorRunningStatus(models.IntegerChoices):
    GOING_UP = 1
    STANDING_STILL = 0
    GOING_DOWN = -1
