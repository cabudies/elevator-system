from django.db import models

from . import enums


class ElevatorSystem(models.Model):
    ## required set of fields (building_name, building_city, building_state, number_of_floors, elevators_count)
    building_name = models.CharField(max_length = 100)
    building_city = models.CharField(max_length = 100)
    building_state = models.CharField(max_length = 100)
    number_of_floors = models.PositiveSmallIntegerField()
    elevators_count = models.PositiveSmallIntegerField()


class Elevator(models.Model):
    ## (fk-elevator system id, elevator_number, current_floor, current_status(enum), is_operational)
    elevator_system = models.ForeignKey(ElevatorSystem, on_delete=models.CASCADE)

    elevator_number = models.PositiveSmallIntegerField()
    current_floor = models.PositiveSmallIntegerField()
    current_status = models.IntegerField(choices=enums.ElevatorRunningStatus.choices, default=0)
    is_operational = models.BooleanField(default=True)


class ElevatorRequest(models.Model):
    ## (fk-elevator, requested_floor)
    elevator = models.ForeignKey(Elevator, on_delete=models.CASCADE)

    requested_floor = models.PositiveSmallIntegerField()

