from django.urls import path, include
from .views import *








urlpatterns = [
    path('public/category/', PublicCategoryView.as_view(), name="public_category"),
    path('public/category/<str:slug>/', PublicCategoryDetailView.as_view(), name="public_category"),
    path('public/organisations/', PublicOrganisationView.as_view(), name="public_organisations"),
    path('public/organisations/<str:slug>/', PublicOrganisationDetailView.as_view(), name="public_organisations"),
    path('public/datasets/', PublicDatasetView.as_view(), name="public_datasets"),
    path('public/datasets/<str:slug>/', PublicDatasetDetailView.as_view(), name="public_datasets"),
    path('public/counts/', PublicCounts.as_view(), name="public_counts"),

]
