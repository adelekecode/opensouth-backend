from django.shortcuts import render
from main.serializers import *
from main.models import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from accounts.permissions import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, AuthenticationFailed, NotFound, ValidationError
from accounts.models import *
from accounts.serializers import *
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination



# Create your views here.



User = get_user_model()



class AdminDatatsetView(generics.ListAPIView):

    permission_classes = [IsAdmin]
    authentication_classes = [JWTAuthentication]
    serializer_class = DatasetSerializer
    queryset = Datasets.objects.filter(is_deleted=False).order_by('-created_at')
    pagination_class = LimitOffsetPagination




class AdminOrganisationView(generics.ListAPIView):

    permission_classes = [IsAdmin]
    authentication_classes = [JWTAuthentication]
    serializer_class = OrganisationSerializer
    queryset = Organisations.objects.filter(is_deleted=False).order_by('-created_at')
    pagination_class = LimitOffsetPagination


    def list(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())
        state = request.GET.get('status', None)

        if state == "approved":
            queryset = queryset.filter(status="approved")

        if state == "rejected":
            queryset = queryset.filter(status="rejected")

        if state == "pending":
            queryset = queryset.filter(status="pending")

        if state == "blocked":
            queryset = queryset.filter(is_active=False)

        if state == "unblocked":
            queryset = queryset.filter(is_active=True)

        if state == "verified":
            queryset = queryset.filter(is_verified=True)

        if state == "unverified":
            queryset = queryset.filter(is_verified=False)

        if state == "undeleted":
            queryset = queryset.filter(is_deleted=False)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = OrganisationSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = OrganisationSerializer(queryset, many=True)

        return Response(serializer.data)



    
    




@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdmin])
def dataset_actions(request, pk, action):

    if request.method == 'POST':
        if pk is None:
            return Response({"error": "dataset id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        if action is None:
            return Response({"error": "action is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            dataset = Datasets.objects.get(id=pk)
        except Datasets.DoesNotExist:
            return Response({"error": "dataset does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        if action == "reject":

            dataset.status = "rejected"
            dataset.save()
            return Response({"message": "dataset rejected successfully"}, status=status.HTTP_200_OK)
        
        elif action == "approve":

            dataset.status = "published"
            dataset.save()
            return Response({"message": "dataset approved successfully"}, status=status.HTTP_200_OK)
        
        elif action == "further_review":
                
            dataset.status = "further_review"
            dataset.save()
            return Response({"message": "dataset kept for further review successfully"}, status=status.HTTP_200_OK)
        
        else:
            return Response({"error": "invalid action"}, status=status.HTTP_400_BAD_REQUEST)
        




@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdmin])
def organisation_actions(request, pk, action):

    if request.method == 'POST':
      
        try:
            organisation = Organisations.objects.get(id=pk)
        except Datasets.DoesNotExist:
            return Response({"error": "organisation does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        if action == "reject":

            organisation.status = "rejected"
            organisation.save()
            
            return Response({"message": "organisation rejected successfully"}, status=status.HTTP_200_OK)
        
        elif action == "approve":

            organisation.status = "approved"
            organisation.save()
            return Response({"message": "organisation approved successfully"}, status=status.HTTP_200_OK)
        
        elif action == "block":

            organisation.is_active = False
            organisation.save()
            return Response({"message": "organisation blocked successfully"}, status=status.HTTP_200_OK)
        
        elif action == "unblock":
                
            organisation.is_active = True
            organisation.save()
            return Response({"message": "organisation unblocked successfully"}, status=status.HTTP_200_OK)
        
        elif action == "delete":
                    
            organisation.is_deleted = True
            organisation.save()
            return Response({"message": "organisation deleted successfully"}, status=status.HTTP_200_OK)

        else:
            return Response({"error": "invalid action"}, status=status.HTTP_400_BAD_REQUEST)
        


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdmin])
def organisation_indicators(request):

    if request.method == 'GET':
      
        data = {
          
        "count": Organisations.objects.filter(is_deleted=False).count(),
        "approved": Organisations.objects.filter(is_deleted=False, status="approved").count(),
        "rejected": Organisations.objects.filter(is_deleted=False, status="rejected").count(),
        "pending": Organisations.objects.filter(is_deleted=False, status="pending").count()
          
    }
        
        return Response(data, status=status.HTTP_200_OK)
    




class NewsView(APIView):

    permission_classes = [IsAdmin]
    authentication_classes = [JWTAuthentication]
    serializer_class = NewsSerializer

    @swagger_auto_schema(request_body=NewsSerializer)
    @action(detail=True, methods=['POST'])
    def post(self, request):
        serializer = NewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "news created successfully"}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class AdminListNewsView(generics.ListAPIView):

    permission_classes = [IsAdmin]
    authentication_classes = [JWTAuthentication]
    pagination_class  = LimitOffsetPagination
    serializer_class = NewsSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    queryset = News.objects.filter(is_deleted=False).order_by('-created_at')



    def list(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())
        state = request.query_params.get('state', None)

        if state == "published":
            queryset = queryset.filter(is_published=True)

        if state == "unpublished":
            queryset = queryset.filter(is_published=False)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = NewsSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = NewsSerializer(queryset, many=True)

        return Response(serializer.data)


   
   

class NewsDetailView(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [IsAdmin]
    authentication_classes = [JWTAuthentication]
    serializer_class = NewsSerializer
    queryset = News.objects.filter(is_deleted=False).order_by('-created_at')
    lookup_field = 'pk'
    


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def news_views(request, pk):

    if request.method == 'POST':
        
        try:
            news = News.objects.get(id=pk)
        except News.DoesNotExist:
            return Response({"error": "news does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        news.views += 1
        news.save()

        return Response({"message": "news views updated successfully"}, status=status.HTTP_200_OK)
    


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdmin])
def news_actions(request, pk, action):

    if request.method == 'POST':
      
        try:
            news = News.objects.get(id=pk)
        except News.DoesNotExist:
            return Response({"error": "news does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        if action == "publish":

            news.is_published = True
            news.save()
            
            return Response({"message": "news objectt updated successfully"}, status=status.HTTP_200_OK)
        
        else:
            return Response({"error": "invalid action"}, status=status.HTTP_400_BAD_REQUEST)
    


    
class AdminOrganisation_Requests(generics.ListAPIView):

    permission_classes = [IsAdmin]
    authentication_classes = [JWTAuthentication]
    serializer_class = OrganisationRequestSerializer
    queryset = OrganisationRequests.objects.filter(is_deleted=False).order_by('-created_at')
    pagination_class = LimitOffsetPagination
    
    def list(self, request, *args, **kwargs):
        pk = request.GET.get('pk', None)
        

        if pk:

            try:
                organisation = Organisations.objects.get(id=pk)
            except Organisations.DoesNotExist:
                return Response({"error": "organisation does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
            queryset = self.filter_queryset(self.get_queryset()).filter(organisation=organisation)

            serializer = OrganisationRequestSerializer(queryset, many=True)

            return Response(serializer.data)
        
        queryset = self.filter_queryset(self.get_queryset())
        serializer = OrganisationRequestSerializer(queryset, many=True)

        return Response(serializer.data)


    