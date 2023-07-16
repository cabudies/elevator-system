from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.ElevatorSystem)
class ElevatorSystemAdmin(admin.ModelAdmin):
    list_display = ('building_name', 'building_state', 'number_of_floors', 'elevators_count')


@admin.register(models.Elevator)
class ElevatorAdmin(admin.ModelAdmin):
    pass
