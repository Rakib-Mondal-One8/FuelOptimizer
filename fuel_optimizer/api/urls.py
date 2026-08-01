from django.urls import path
from . import views

urlpatterns = [
    path('FuelStation/',views.FuelStationView.as_view(),name="FuelStation"),
]