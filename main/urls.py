from django.urls import path, include
from .views import *

urlpatterns = [
   path('organisations/', OrganisationView.as_view(), name="organisations"),
]
