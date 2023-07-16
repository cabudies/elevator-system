from django.db import models

# Create your models here.
class ElevatorSystem(models.Model):
    pass
    ## required set of fields (building_name, building_city, building_state, number_of_floors, elevators_count)

class Elevator(models.Model):
    pass
    ## required set of fields
    ## (fk-elevator system id, elevator_number, current_floor, current_status(enum), is_operational)


class ElevatorRequest(models.Model):
    pass
    ## required set of fields
    ## (fk-elevator, requested_floor)

