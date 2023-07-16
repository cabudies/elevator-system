from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework import status

from . import models, enums, serializers


class ElevatorSystemViewSet(ModelViewSet):
    queryset = models.ElevatorSystem.objects.all()
    serializer_class = serializers.ElevatorSystemSerializer
    permission_classes = (AllowAny,)
    
    
    def get_queryset(self):
        elevator_system_id = self.request.query_params.get('id')
        queryset = self.queryset
        
        if elevator_system_id:
            queryset = queryset.filter(id=int(elevator_system_id))
        
        return queryset.order_by('id')
    

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            serializer.data, 
            status=status.HTTP_201_CREATED
        )


class ElevatorViewSet(ModelViewSet):
    queryset = models.Elevator.objects.all()
    serializer_class = serializers.ElevatorSerializer
    permission_classes = (AllowAny,)
    

    def get_queryset(self):
        elevator_id = self.request.query_params.get('elevator_id')
        elevator_system_id = self.request.query_params.get('elevator_system')

        queryset = self.queryset

        if elevator_id:
            queryset = queryset.filter(id=int(elevator_id))
        
        if elevator_system_id:
            queryset = queryset.filter(elevator_system=int(elevator_system_id))
        
        return queryset.order_by('id')
    

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            serializer.data, 
            status=status.HTTP_201_CREATED
        )


class ElevatorRequestViewSet(ModelViewSet):
    queryset = models.ElevatorRequest.objects.all()
    serializer_class = serializers.ElevatorRequestSerializer
    permission_classes = (AllowAny,)
    
    def list(self, request):
        serializer = serializers.ElevatorRequestSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        item = get_object_or_404(self.queryset, pk=pk)
        serializer = serializers.ElevatorRequestSerializer(item)
        return Response(serializer.data)
    
    def get_specified_elevator_details(self, elevator_id):
        elevator_records = models.Elevator.objects.filter(
            id=elevator_id
        )
        elevator_records_serialized = serializers.ElevatorSerializer(elevator_records[0])
        
        result = elevator_records_serialized.data
        
        return result
    

    def get_specified_elevator_system_details(self, elevator_system_id):
        elevator_system_records = models.ElevatorSystem.objects.filter(
            id=elevator_system_id
        )
        elevator_system_records_serialized = serializers.ElevatorSystemSerializer(elevator_system_records[0])
        
        result = elevator_system_records_serialized.data
        return result 


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        ## valid the request if the lift is going up or standing still, accept the request
        ## else reject the request if the lift is going down
        ## if the lift is on same floor, open the doors
        elevator_details = self.get_specified_elevator_details(
            elevator_id=request.data["elevator"]
        )
        
        elevator_system_details = self.get_specified_elevator_system_details(
            elevator_system_id=elevator_details["elevator_system"]
        )

        elevator_current_status = elevator_details["current_status"]
        
        if request.data["requested_floor"] > elevator_system_details["number_of_floors"]:
            return Response(
                {
                    "error": "Invalid floor number is provided"
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        elif request.data["requested_floor"] < 0:
            return Response(
                {
                    "error": "Invalid floor number is provided"
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if request.data["requested_floor"] == elevator_details["current_floor"]:
            elevator_current_status = enums.ElevatorRunningStatus.STANDING_STILL
        elif request.data["requested_floor"] < elevator_details["current_floor"]:
            elevator_current_status = enums.ElevatorRunningStatus.GOING_DOWN
        elif request.data["requested_floor"] > elevator_details["current_floor"]:
            elevator_current_status = enums.ElevatorRunningStatus.GOING_UP
        
        elevator_db_record = models.Elevator.objects.get(id=request.data["elevator"])
        elevator_db_record.current_floor = request.data["requested_floor"]
        elevator_db_record.current_status = elevator_current_status
        elevator_db_record.save()

        self.perform_create(serializer)

        return Response(
            serializer.data, 
            status=status.HTTP_201_CREATED
        )
