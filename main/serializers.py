from .models import *
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()






class OrganisationSeriializer(serializers.ModelSerializer):


    logo = serializers.ImageField(required=False)
    data_count = serializers.ReadOnlyField()
    users_data = serializers.ReadOnlyField()
    logo_url = serializers.ReadOnlyField()


    

    class Meta:
        model = Organisations
        fields = "__all__"



class DatasetSerializer(serializers.ModelSerializer):

    files_count = serializers.ReadOnlyField()
    publisher_data = serializers.ReadOnlyField()
    views = serializers.ReadOnlyField()
    files = serializers.ReadOnlyField()

    


    class Meta:
        model = Datasets
        fields = "__all__"



class DatasetFileSerializer(serializers.ModelSerializer):

    dataset_data = serializers.ReadOnlyField()
    uploaded_by = serializers.ReadOnlyField()
    file_url = serializers.ReadOnlyField()
    file = serializers.FileField(required=True)

    class Meta:
        model = DatasetFiles
        fields = "__all__"




class CategorySerializer(serializers.ModelSerializer):

    data_count = serializers.ReadOnlyField()

    class Meta:
        model = Categories
        fields = "__all__"


class DatasetViewsSerializer(serializers.ModelSerializer):

    dataset_data = serializers.ReadOnlyField()
    class Meta:
        model = DatasetViews
        fields = "__all__"



class TagsSerializer(serializers.ModelSerializer):

    keywords = serializers.ListField(child=serializers.CharField(max_length=100), required=True)

    class Meta:
        model = Tags
        fields = "__all__"