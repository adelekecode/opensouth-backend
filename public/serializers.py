from rest_framework import serializers
from main.models import Tags, Support











class PublicTagSerializer(serializers.Serializer):

    class Meta:
        model = Tags
        fields = "__all__"


