from django.urls import path, include
from .views import *








urlpatterns = [
    path('admin/datasets/', AdminDatatsetView.as_view(), name="admin_datatsets"),
    path('admin/datasets/pk/<uuid:pk>/actions/<str:action>/', dataset_actions, name="admin_datatsets_actions"),
    path('admin/organisations/pk/<uuid:pk>/actions/<str:action>/', organisation_actions, name="admin_organisations_actions"),
    path('admin/organisations/', AdminOrganisationView.as_view(), name="admin_organisations"),
    
]
