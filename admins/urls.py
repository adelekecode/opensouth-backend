from django.urls import path, include
from .views import *








urlpatterns = [
    path('admin/datatsets/', AdminDatatsetView.as_view(), name="admin_datatsets"),
    path('admin/datatsets/pk/<uuid:pk>/actions/<str:action>/', dataset_actions, name="admin_datatsets_actions"),
    
]
