from django.shortcuts import render
from .serializers import *
from .models import *
from accounts.serializers import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from accounts.permissions import *
from .email import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import get_user_model
from rest_framework.exceptions import PermissionDenied, AuthenticationFailed, NotFound, ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from accounts.permissions import *
from djoser.views import UserViewSet
from rest_framework.views import APIView
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import Permission, Group
from django.db.models import Q
import requests
import os

# Create your views here.




User = get_user_model()

class CategoryView(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(methods=['POST'], request_body=CategorySerializer())
    @action(detail=True, methods=['POST'])
    def post(self, request):
        if request.user.role != "admin":
            return Response({"error": "you are not authorised to create category"}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        name = serializer.validated_data['name']
        slug = slugify(name)

        if Categories.objects.filter(slug=slug).exists():
            return Response({"error": "Category with this name already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

    def get(self, request):

        categories = Categories.objects.filter(is_deleted=False)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [IsAdmin]
    authentication_classes = [JWTAuthentication]
    serializer_class = CategorySerializer
    queryset = Categories.objects.filter(is_deleted=False)
    lookup_field = 'pk'


class OrganisationView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(methods=['POST'], request_body=OrganisationSeriializer())
    @action(detail=True, methods=['POST'])
    def post(self, request):

        serializer = OrganisationSeriializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        name = serializer.validated_data['name']
        slug = slugify(name)

        if Organisations.objects.filter(slug=slug).exists():
            return Response({"error": "Organisation with this name already exists"}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        serializer.instance.users.add(request.user)
        serializer.instance.user = request.user
        serializer.instance.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

    def get(self, request):
        organisations = Organisations.objects.filter(users=request.user, is_deleted=False)
        serializer = OrganisationSeriializer(organisations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    




class OrganisationDetailView(generics.RetrieveUpdateDestroyAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = OrganisationSeriializer
    queryset = Organisations.objects.filter(is_deleted=False)
    lookup_field = 'pk'




@swagger_auto_schema(methods=['POST'], request_body=EmailSerializer())
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def add_user_to_organisation(request, org_pk):

    if request.method == "POST":
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        
        try:
            organisation = Organisations.objects.get(pk=org_pk)
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "user does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Organisations.DoesNotExist:
            return Response({"error": "organisation does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        if organisation.user != request.user:
            return Response({"error": "you are not authorised to add user to this organisation"}, status=status.HTTP_401_UNAUTHORIZED)


        if organisation.users.filter(pk=user.id).exists():
            return Response({"error": "user already exists in user list"}, status=status.HTTP_400_BAD_REQUEST)
        
        organisation.users.add(user)
        organisation_add_users(organisation=organisation, user=user)
        return Response({"message": "user added successfully"}, status=status.HTTP_200_OK)



@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_user_from_organisation(request, org_pk, user_pk):
    
    if request.method == "DELETE":
        
        try:
            organisation = Organisations.objects.get(pk=org_pk)
            user = User.objects.get(pk=user_pk)
        except User.DoesNotExist:
            return Response({"error": "user does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Organisations.DoesNotExist:
            return Response({"error": "organisation does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        if organisation.user != request.user:
            return Response({"error": "you are not authorised to delete user from this organisation"}, status=status.HTTP_401_UNAUTHORIZED)

        if organisation.users.filter(pk=user.id).exists():
            organisation.users.remove(user)
            organisation_delete_users(organisation=organisation, user=user)

            return Response({"message": "user removed successfully"}, status=status.HTTP_200_OK)
        
        return Response({"error": "user does not exist in user list"}, status=status.HTTP_400_BAD_REQUEST)




class DatasetView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(methods=['POST'], request_body=DatasetSerializer())
    @action(detail=True, methods=['POST'])
    def post(self, request):
        
        serializer = DatasetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        category_id = data['category_id']
        organisation_id = data['organisation_id']
        title = data['title']
        slug = slugify(title)

        if Datasets.objects.filter(slug=slug).exists():
            return Response({"error": "dataset with this title already exists"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            category = Categories.objects.get(pk=category_id)
        except Categories.DoesNotExist:
            return Response({"error": "category does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        if organisation_id != None:
            try:
                organisation = Organisations.objects.get(pk=organisation_id)
            except Organisations.DoesNotExist:
                return Response({"error": "organisation does not exist"}, status=status.HTTP_404_NOT_FOUND)
            serializer.validated_data['organisation'] = organisation

        serializer.validated_data['user'] = request.user
        serializer.validated_data['category'] = category
        serializer.save()


        return Response(serializer.data, status=status.HTTP_201_CREATED)

      


class CreateDatasetFiles(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(methods=['POST'], request_body=DatasetFileSerializer())
    @action(detail=True, methods=['POST'])
    def post(self, request, pk):

        serializer = DatasetFileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            dataset = Datasets.objects.get(pk=pk)
        except Datasets.DoesNotExist:
            return Response({"error": "dataset instance not found"}, status=400)
        serializer.validated_data["dataset"] = dataset
        serializer.validated_data["uploaded_by"] = request.user

        serializer.save()

        data = {
            "message": "file uploaded successfully",
            "data": serializer.data
        }
        return Response(data, status=200)






class DatasetViewsView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(methods=['POST'], request_body=DatasetViewsSerializer())
    @action(detail=True, methods=['POST'])
    def post(self, request, pk):

        try:
            dataset = Datasets.objects.get(pk=pk)
        except Datasets.DoesNotExist:
            return Response({"error": "dataset instance not found"}, status=400)
        
        dataset_view = DatasetViews.objects.filter(dataset=dataset)

        if dataset_view.exists():
            dataset_view = dataset_view.first()
            dataset_view.views += 1
            dataset_view.save()
            return Response({"message": "dataset view updated"}, status=200)
        else:
            dataset_view = DatasetViews.objects.create(dataset=dataset)
            dataset_view.views += 1
            dataset_view.save()

            return Response({"message": "dataset views updated"}, status=200)

        