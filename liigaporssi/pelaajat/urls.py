from django.urls import path
from .views import satunnaiset_pelaajat

urlpatterns = [
    path('satunnaiset/', satunnaiset_pelaajat, name='satunnaiset_pelaajat')
]