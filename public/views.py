from django.shortcuts import render
from main.serializers import *
from main.models import *
from rest_framework import status
from rest_framework.response import Response
from accounts.permissions import *
from rest_framework.decorators import api_view, authentication_classes, permission_classes
# from accounts.permissions import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, AuthenticationFailed, NotFound, ValidationError
from accounts.models import *
from accounts.serializers import *
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from datetime import datetime
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
# Create your views here.




User = get_user_model()




class PublicCategoryView(APIView):

    permission_classes = [PublicPermissions]

    def get(self, request):
        categories = Categories.objects.filter(is_deleted=False).order_by('-created_at')
        serializer = CategorySerializer(categories, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class PublicCategoryDetailView(generics.RetrieveAPIView):
    
    permission_classes = [PublicPermissions]
    serializer_class = CategorySerializer
    queryset = Categories.objects.filter(is_deleted=False).order_by('-created_at')
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'




class PublicOrganisationView(generics.ListAPIView):

    permission_classes = [PublicPermissions]
    serializer_class = OrganisationSerializer
    queryset = Organisations.objects.filter(is_deleted=False, status='approved').order_by('-created_at')
    pagination_class = LimitOffsetPagination


class PublicOrganisationDetailView(generics.RetrieveAPIView):

    permission_classes = [PublicPermissions]
    serializer_class = OrganisationSerializer
    queryset = Organisations.objects.filter(is_deleted=False, status='approved').order_by('-created_at')
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'


class PublicDatasetView(generics.ListAPIView):

    permission_classes = [PublicPermissions]
    serializer_class = DatasetSerializer
    queryset = Datasets.objects.filter(is_deleted=False, status='published').order_by('-created_at')
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    # filterset_fields = ['category']
    search_fields = ['title', 'category__name', 'tags__name']


    def list(self, request, *args, **kwargs):

        category = request.GET.get('category', None)
        organisation = request.GET.get('organisation', None)
        tags = request.GET.get('tags', None)
        start_date = request.GET.get('start_date', None)
        end_date = request.GET.get('end_date', None)
        format = request.GET.get('format', None)
        spatial_coverage = request.GET.get('spatial_coverage', None)

        
        queryset = self.filter_queryset(self.get_queryset())

        if category:
            queryset = queryset.filter(category__name=category)

        if organisation:
            queryset = queryset.filter(organisation__name=organisation)

        if tags:
            queryset = queryset.filter(tags__name=tags)

        if spatial_coverage:
            queryset = queryset.filter(spatial_coverage=spatial_coverage)

        if format:
            queryset = queryset.filter(format=format)

        if start_date and end_date:
            Start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            End_date = datetime.strptime(end_date, "%Y-%m-%d").date()
            queryset = queryset.filter(created_at__range=[Start_date, End_date])


        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)
    

class PublicDatasetDetailView(generics.RetrieveAPIView):
    
    permission_classes = [PublicPermissions]
    serializer_class = DatasetSerializer
    queryset = Datasets.objects.filter(is_deleted=False, status='published').order_by('-created_at')
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'

        





class PublicCounts(APIView):
    permission_classes = [PublicPermissions]

    def get(self, request):

        data = {
            "datasets": Datasets.objects.filter(is_deleted=False, status='published').count(),
            "organisations": Organisations.objects.filter(is_deleted=False, status='approved').count(),
            "users": User.objects.filter(is_deleted=False).count(),
            "categories": Categories.objects.filter(is_deleted=False).count(),
            "files": DatasetFiles.objects.filter(is_deleted=False).count(),
        }

        return Response(data, status=status.HTTP_200_OK)






class PopularDataset(APIView):

    permission_classes = [PublicPermissions]

    def get(self, request):

        views = DatasetViews.objects.all().order_by('-count')[:9]
        serializer = DatasetViewsSerializer(views, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK) 
    



class PublicNews(APIView):

    permission_classes = [PublicPermissions]

    def get(self, request):

        news = News.objects.filter(is_deleted=False, is_published=True).order_by('-created_at')
        serializer = NewsSerializer(news, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    

class PublicNewsDetailView(generics.RetrieveAPIView):
    
    permission_classes = [PublicPermissions]
    serializer_class = NewsSerializer
    queryset = News.objects.filter(is_deleted=False, is_published=True).order_by('-created_at')
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'