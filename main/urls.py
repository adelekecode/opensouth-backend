from django.urls import path, include
from .views import *








urlpatterns = [
    path('organisations/', OrganisationView.as_view(), name="organisations"),
    path('organisations/<uuid:pk>/', OrganisationView.as_view(), name="organisations"),
    path('organisations/<uuid:org_pk>/users/<str:user_pk>/', add_delete_user_to_organisation, name="add_delete_user_to_organisation"),
    path('datasets/', DatasetView.as_view(), name="datasets"),
    path('datasets/files/<uuid:pk>/', CreateDatasetFiles.as_view(), name="datasets_files"),
    path('categories/', CategoryView.as_view(), name="categories"),
    path('categories/<uuid:pk>/', CategoryDetailView.as_view(), name="categories"),
]
