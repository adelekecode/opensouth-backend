import hashlib
from django.shortcuts import render
from .serializers import *
from .models import *
from django.db import IntegrityError
from accounts.serializers import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from accounts.permissions import *
from .email import *
from .helpers import *
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
from rest_framework.pagination import LimitOffsetPagination
import requests
import os

# Create your views here.






User = get_user_model()

class CategoryView(APIView):

    # permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = CategorySerializer
    queryset = Categories.objects.filter(is_deleted=False)

    @swagger_auto_schema(methods=['POST'], request_body=CategorySerializer())
    @action(detail=True, methods=['POST'])
    def post(self, request):
        # if request.user.role != "admin":
        #     return Response({"error": "you are not authorised to create category"}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        name = serializer.validated_data['name']
        slug = slugify(name)

        if Categories.objects.filter(slug=slug).exists():
            return Response({"error": "Category with this name already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

    def get(self, request):

        categories = Categories.objects.filter(is_deleted=False).order_by('-created_at')
        serializer = CategorySerializer(categories, many=True)

        data = {
            "count": categories.count(),
            "data": serializer.data
        }

        return Response(data, status=status.HTTP_200_OK)
    


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [IsAdmin]
    authentication_classes = [JWTAuthentication]
    serializer_class = CategorySerializer
    queryset = Categories.objects.filter(is_deleted=False)
    lookup_field = 'pk'


class OrganisationView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


    @swagger_auto_schema(methods=['POST'], request_body=OrganisationSerializer())
    @action(detail=True, methods=['POST'])
    def post(self, request):

        serializer = OrganisationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        name = serializer.validated_data['name']
        email = serializer.validated_data['email']
        type = serializer.validated_data['type']
        slug = slugify(name)

        username, domain = email.split('@')

        if domain == "gmail.com":
            if type == "cooperate_organisation":
                return Response({"error": "gmail is not allowed for cooperate organisations"}, status=status.HTTP_400_BAD_REQUEST)

        if Organisations.objects.filter(slug=slug).exists():
            return Response({"error": "Organisation with this name already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save(
            user = request.user
        )

        serializer.instance.users.add(request.user)
        serializer.instance.save()

  
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
    




class OrganisationDetailView(generics.RetrieveUpdateDestroyAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = OrganisationSerializer
    queryset = Organisations.objects.filter(is_deleted=False)
    lookup_field = 'slug'




@swagger_auto_schema(methods=['POST'], request_body=EmailSerializer())
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdmin])
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
      

        if organisation.users.filter(pk=user.id).exists():
            return Response({"error": "user already exists in user list"}, status=status.HTTP_400_BAD_REQUEST)
        
        organisation.users.add(user)
        organisation_add_users(organisation=organisation, user=user)

        return Response({"message": "user added successfully"}, status=status.HTTP_200_OK)



@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdmin])
def delete_user_from_organisation(request, org_pk, user_pk):
    
    if request.method == "DELETE":
        
        try:
            organisation = Organisations.objects.get(pk=org_pk)
            user = User.objects.get(pk=user_pk)
        except User.DoesNotExist:
            return Response({"error": "user does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Organisations.DoesNotExist:
            return Response({"error": "organisation does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
     
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
    def post(self, request, cat_pk):
        
        serializer = DatasetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        coordinates = request.data.get('coordinates')
        country = data['spatial_coverage']

        organisation = request.GET.get('organisation_id', None)

       
        title = data['title']
        slug = slugify(title)

        if Datasets.objects.filter(slug=slug).exists():
            return Response({"error": "dataset with this title already exists"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            category = Categories.objects.get(pk=cat_pk)
        except Categories.DoesNotExist:
            return Response({"error": "category does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        if organisation:

            try:
                organisation = Organisations.objects.get(pk=organisation)
            except Organisations.DoesNotExist:

                return Response({"error": "organisation does not exist"}, status=status.HTTP_404_NOT_FOUND)
            
            if request.user not in organisation.users.all():
                return Response({"error": "you are not authorised to create dataset for this organisation"}, status=status.HTTP_401_UNAUTHORIZED)
            
            if organisation.status != "approved":
                return Response({"error": "organisation is not verified"}, status=status.HTTP_401_UNAUTHORIZED)
            

            serializer.validated_data['organisation'] = organisation

        serializer.validated_data['user'] = request.user
        serializer.validated_data['category'] = category
        serializer.validated_data['geojson'] = {

            "country": country,
            "coordinates": coordinates
        }
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
       

        file = serializer.validated_data['file']
        format = serializer.validated_data['format']
        size = serializer.validated_data['size']


        try:
            d_set = DatasetFiles.objects.create(
                dataset=dataset,
                user=request.user,  
                file=file,
                format=format,
                size=size
              
            )
        except Exception as e:
            return Response({"error": str(e)}, status=400)
       

        data = {
            "message": "file uploaded successfully",
            "data": DatasetFileSerializer(d_set).data
        }
        return Response(data, status=200)






class DatasetViewsView(APIView):


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
            dataset_view.count += 1
            dataset_view.save()
            
            return Response({"message": "dataset view updated"}, status=200)
        
        else:
            dataset_view = DatasetViews.objects.create(dataset=dataset)
            dataset_view.count += 1
            dataset_view.save()

            return Response({"message": "dataset views updated"}, status=200)

        


class TagsView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(methods=['POST'], request_body=TagsSerializer())
    @action(detail=True, methods=['POST'])
    def post(self, request, pk):

        serializers = TagsSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)

        try:
            dataset = Datasets.objects.get(pk=pk)
        except Datasets.DoesNotExist:
            return Response({"error": "dataset instance not found"}, status=400)
        
        tags = serializers.validated_data['keywords']

        for tag in tags:
            slug = slugify(tag)
            if Tags.objects.filter(slug=slug).exists():
                tag = Tags.objects.get(slug=slug)
                dataset.tags.add(tag)
            else:
                tag = Tags.objects.create(name=tag)
                dataset.tags.add(tag)

        return Response({"message": "tags added successfully"}, status=200)
    

    def delete(self, request, pk):

        serializers = TagsSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)

        try:
            dataset = Datasets.objects.get(pk=pk)
        except Datasets.DoesNotExist:
            return Response({"error": "dataset instance not found"}, status=400)
        
        tags = serializers.validated_data['keywords']

        for tag in tags:
            slug = slugify(tag)
            if Tags.objects.filter(slug=slug).exists():
                tag = Tags.objects.get(slug=slug)
                dataset.tags.remove(tag)
            else:
                return Response({"error": f"tag does not exist {tag}"}, status=400)

        return Response({"message": "tags removed successfully"}, status=200)




class UserDataset(generics.ListAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = DatasetSerializer
    queryset = Datasets.objects.filter(is_deleted=False)

    def get_queryset(self):
        return Datasets.objects.filter(user=self.request.user, is_deleted=False).order_by('-created_at')
    


class UserOrganisation(generics.ListAPIView):

    authentication_classes = [JWTAuthentication]
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAuthenticated]
    serializer_class = OrganisationSerializer
    queryset = Organisations.objects.filter(is_deleted=False)

    def get_queryset(self):
        return Organisations.objects.filter(users=self.request.user, is_deleted=False).order_by('-created_at')
    



class UserOrganisationDatasets(generics.ListAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = DatasetSerializer
    queryset = Datasets.objects.filter(is_deleted=False)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        pk = self.kwargs['pk']

        try:
            organisation = Organisations.objects.get(pk=pk)
        except Organisations.DoesNotExist:
            return Response({"error": "organisation does not exist"}, status=404)
        
        if self.request.user not in organisation.users.all():
            return Response({"error": "you are not authorised to view this"}, status=401)
        

        return Datasets.objects.filter(organisation=organisation, is_deleted=False).order_by('-created_at')
    


class DatasetDownloadCount(APIView):


    def post(self, request, pk):

        files = get_object_or_404(DatasetFiles, pk=pk)

        files.download_count += 1
        files.save()

        return Response({"message": "download count updated"}, status=200)
    

        

class OrganisationVerification(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):

        if request.method == 'PUT':

            serializer = PinSerializer(data=request.data)
            if serializer.is_valid():

                data = serializer.verify_pin(request)

                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            




@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def resend_pin(request, pk):
    if request.method == 'POST':

        try:
            organisation = Organisations.objects.get(pk=pk)
        except Organisations.DoesNotExist:
            return Response({"error": "organisation does not exist"}, status=404)
        
        if organisation.is_verified:
            return Response({"error": "organisation already verified"}, status=400)
        
        pin = generate_organisation_pin(organisation=organisation)
        organisation_verification_email(email=organisation.email, user=organisation.user, organization=organisation, pin=pin)

        return Response({"message": "pin resent successfully"}, status=200)
        
        