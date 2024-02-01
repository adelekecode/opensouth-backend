from .models import *
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()






class OrganisationSerializer(serializers.ModelSerializer):


    logo = serializers.ImageField(required=False)
    data_count = serializers.ReadOnlyField()
    downloads_count = serializers.ReadOnlyField()
    views_count = serializers.ReadOnlyField()
    users_data = serializers.ReadOnlyField()
    logo_url = serializers.ReadOnlyField()
    email = serializers.EmailField(required=True)

    

    class Meta:
        model = Organisations
        fields = "__all__"



class DatasetSerializer(serializers.ModelSerializer):

    coordinates = serializers.CharField(read_only=True)

    
    publisher_data = serializers.ReadOnlyField()
    files = serializers.ReadOnlyField()
    tags_data = serializers.ReadOnlyField()
    views = serializers.ReadOnlyField()
    files_count = serializers.ReadOnlyField()

    


    class Meta:
        model = Datasets
        fields = "__all__"



class DatasetFileSerializer(serializers.ModelSerializer):

    dataset_data = serializers.ReadOnlyField()
    file_url = serializers.ReadOnlyField()
    file = serializers.FileField(required=True)
    uploaded_by = serializers.ReadOnlyField()

    class Meta:
        model = DatasetFiles
        fields = "__all__"

  
        




class CategorySerializer(serializers.ModelSerializer):

    data_count = serializers.ReadOnlyField()
    image_url = serializers.ReadOnlyField()

    class Meta:
        model = Categories
        fields = "__all__"


class DatasetViewsSerializer(serializers.ModelSerializer):

    dataset_data = serializers.ReadOnlyField()
    class Meta:
        model = DatasetViews
        fields = "__all__"



class TagsSerializer(serializers.ModelSerializer):

    keywords = serializers.ListField(child=serializers.CharField(max_length=100), required=True, read_only=True)
    name = serializers.CharField(max_length=100, required=False)

    class Meta:
        model = Tags
        fields = "__all__"







class PinSerializer(serializers.Serializer):

    pin = serializers.CharField(max_length=6, required=True)



class DatasetCommentSerializer(serializers.ModelSerializer):

    dataset_data = serializers.ReadOnlyField()
    user_data = serializers.ReadOnlyField()
    
    class Meta:
        model = DatasetComments
        fields = "__all__"




class NewsSerializer(serializers.ModelSerializer):

    image_url = serializers.ReadOnlyField()

    class Meta:
        model = News
        fields = "__all__"



class OrganisationRequestSerializer(serializers.ModelSerializer):

    # organisation_data = serializers.ReadOnlyField()
    # user_data = serializers.ReadOnlyField()

    class Meta:
        model = OrganisationRequests
        fields = "__all__"