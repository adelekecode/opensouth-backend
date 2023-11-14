from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import get_user_model
from rest_framework.exceptions import PermissionDenied, AuthenticationFailed, NotFound, ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
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




class OrganisationView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(methods=['POST'], request_body=OrganisationSeriializer())
    @action(detail=True, methods=['POST'])
    def post(self, request):

        serializer = OrganisationSeriializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        name = serializer.validated_data['name']

        if Organisations.objects.filter(name=name).exists():
            return Response({"error": "Organisation with this name already exists"}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        serializer.instance.users.add(request.user)
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





@api_view(['POST', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def add_delete_user_to_organisation(request, org_pk, user_pk):
    if request.method == "POST":
        organisation = Organisations.objects.get(pk=org_pk, users=request.user)
        try:
            user = User.objects.get(pk=user_pk)
        except User.DoesNotExist:
            return Response({"error": "user does not exist"}, status=status.HTTP_404_NOT_FOUND)


        if organisation.users.filter(pk=user.id).exists():
            return Response({"error": "user already exists in user list"}, status=status.HTTP_400_BAD_REQUEST)
        organisation.users.add(user)
        return Response({"message": "user added successfully"}, status=status.HTTP_200_OK)
    
    
    elif request.method == "DELETE":
        organisation = Organisations.objects.get(pk=org_pk, users=request.user)
        try:
            user = User.objects.get(pk=user_pk)
        except User.DoesNotExist:
            return Response({"error": "user does not exist"}, status=status.HTTP_404_NOT_FOUND)

        if organisation.users.filter(pk=user.id).exists():
            organisation.users.remove(user)
            return Response({"message": "user removed successfully"}, status=status.HTTP_200_OK)
        return Response({"error": "user does not exist in user list"}, status=status.HTTP_404_NOT_FOUND)




class DatasetView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(methods=['POST'], request_body=DatasetSerializer())
    @action(detail=True, methods=['POST'])
    def post(self, request):
        
        serializer = DatasetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        if organisation in data:
            organisation_id = data['organisation_id']
        try:
            organisation = Organisations.objects.get(pk=organisation_id)
        except Organisations.DoesNotExist:
            return Response({"error": "organisation instance not found"}, status=400)
        
        if not organisation.users.filter(pk=request.user.id).exists():
            return Response({"error": "you are not authorised to create dataset for this organisation"}, status=status.HTTP_401_UNAUTHORIZED)
        if Datasets.objects.filter(title=data['title'], organisation=organisation).exists():
            return Response({"error": "dataset with this name already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.validated_data["publisher"] = request.user
        serializer.validated_data["organisation"] = organisation if organisation is not None else None
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



