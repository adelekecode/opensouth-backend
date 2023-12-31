from django.urls import path, include
from .views import *








urlpatterns = [
    path('organisations/', OrganisationView.as_view(), name="organisations"),
    path('organisations/<uuid:pk>/', OrganisationDetailView.as_view(), name="organisations"),
    path('organisations/<uuid:org_pk>/users/', add_user_to_organisation, name="add_user_to_organisation"),
    path('organisations/<uuid:org_pk>/users/<str:user_pk>/', delete_user_from_organisation, name="delete_user_from_organisation"),
    path('datasets/<uuid:cat_pk>/', DatasetView.as_view(), name="datasets"),
    path('datasets/files/<uuid:pk>/', CreateDatasetFiles.as_view(), name="datasets_files"),
    path('categories/', CategoryView.as_view(), name="categories"),
    path('categories/<uuid:pk>/', CategoryDetailView.as_view(), name="categories"),
    path('datasets/views/<uuid:pk>/', DatasetViews.as_view(), name="datasets_views"),
    path('datasets/tags/<uuid:pk>/', TagsView.as_view(), name="tags"),
    path('user/organisations/<uuid:pk>/datasets/', UserOrganisationDatasets.as_view(), name="user_organisation_datasets"),
    path('user/datasets/', UserDataset.as_view(), name="user_datasets"),
    path('user/organisations/', UserOrganisation.as_view(), name="user_organisations"),

]
