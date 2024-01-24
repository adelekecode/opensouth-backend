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
    queryset = News.objects.filter(is_deleted=False).order_by('-created_at')
   

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
    


    



       
                

            
