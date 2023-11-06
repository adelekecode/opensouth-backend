from typing import Any
from django.db import models
from django.contrib.auth import get_user_model
import uuid 
from django.forms import model_to_dict
# Create your models here.



User = get_user_model()





class Organisations(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="organisations")
    name = models.CharField(max_length=650)
    description = models.TextField()
    logo = models.ImageField(upload_to="organisation_logo/", blank=True, null=True)
    users = models.ManyToManyField(User, related_name="organisations_users", blank=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name
    
    def delete(self):
        self.is_deleted = True
        self.save()
    
    @property
    def logo_url(self):
        if self.logo:
            return self.logo.url
        return ""
    
    @property
    def users_data(self):
        return [model_to_dict(user, fields=["id", "first_name", "last_name", "email", "role"]) for user in self.users.all()]


    

    






class Datasets(models.Model):

    status_choices = (
        ("pending", "pending"),
        ("further_review", "further_review"),
        ("published", "published"),
        ("rejected", "rejected"),
    )



    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    published_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="publisher")
    title = models.CharField(max_length=650)
    license = models.CharField(max_length=650)
    description = models.TextField()
    update_frequency = models.CharField(max_length=650)
    image = models.ImageField(upload_to="dataset_images/", blank=True, null=True)
    organisation = models.ForeignKey(Organisations, on_delete=models.CASCADE, null=True, related_name="organisation_datasets")
    status = models.CharField(max_length=650, choices=status_choices, default="pending")
    tags = models.ManyToManyField("Tags", related_name="dataset_tags", blank=True)
    temporal_coverage = models.CharField(max_length=650)
    spatial_coverage = models.CharField(max_length=650)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.title} -- {self.status} -- {self.published_by.email}"
    
    def delete(self):
        self.is_deleted = True
        self.save()

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return ""
    
    @property
    def tags_data(self):
        return [model_to_dict(tag, fields=["id", "name"]) for tag in self.tags.all()]
    
    @property
    def organisation_data(self):
        if self.organisation:
            return model_to_dict(self.organisation, fields=["id", "name", "description", "logo_url", "users_data"])
        return None
    
    @property
    def publisher_data(self):
        return model_to_dict(self.published_by, fields=["id", "first_name", "last_name", "email", "role", "image_url"])
    
    


class Tags(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=650)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name
    

    def delete(self):
        self.is_deleted = True
        self.save()
        
    
