from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'elevator-system', views.ElevatorSystemViewSet)
router.register(r'elevator', views.ElevatorViewSet)
router.register(r'elevator-request', views.ElevatorRequestViewSet)


urlpatterns = [
    path('', include(router.urls)),
]