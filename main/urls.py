from django.urls import path, include
from .views import *








urlpatterns = [
    path('organisations/', OrganisationView.as_view(), name="organisations"),
    path('organisations/<str:pk>/', OrganisationView.as_view(), name="organisations"),
    path('organisations/<str:org_pk>/users/<str:user_pk>/', add_delete_user_to_organisation, name="add_delete_user_to_organisation"),
]
