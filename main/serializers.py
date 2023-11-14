from .models import *
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()






class OrganisationSeriializer(serializers.ModelSerializer):

    users_data = serializers.ReadOnlyField()
    logo = serializers.ImageField(required=False)
    

    class Meta:
        model = Organisations
        fields = "__all__"



class DatasetSerializer(serializers.ModelSerializer):

    publisher_data = serializers.ReadOnlyField()
    organisation_data = serializers.ReadOnlyField()
    organisation_id = serializers.CharField(required=False)


    class Meta:
        model = Datasets
        fields = "__all__"



class DatasetFileSerializer(serializers.ModelSerializer):

    dataset_data = serializers.ReadOnlyField()
    file_url = serializers.ReadOnlyField()
    file = serializers.FileField(required=True)

    class Meta:
        model = DatasetFiles
        fields = "__all__"
