from typing import Any
from django.db import models
from django.contrib.auth import get_user_model
import uuid 
from django.forms import model_to_dict
from django.utils.text import slugify
# Create your models here.



User = get_user_model()



class Categories(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=650)
    slug = models.SlugField(max_length=650, null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)

        super(Categories, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"
    
    def delete(self):
        self.is_deleted = True
        self.save()

    






class Organisations(models.Model):

    """ users is the group of users that are in the organisation
        user is the owner of the organisation and the person who has administartive rights to the organisation
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=650)
    slug = models.SlugField(max_length=650, null=True)
    description = models.TextField()
    logo = models.ImageField(upload_to="organisation_logo/", null=True)
    users = models.ManyToManyField(User, related_name="organisations_users", blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="organisation_user")
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)

        super(Organisations, self).save(*args, **kwargs)


    def __str__(self):
        return self.name
    
    def delete(self):
        self.is_deleted = True
        self.save()
    
    @property
    def users_data(self):
        list_data = []
        users = self.users.all()
        for user in users:
            data = model_to_dict(user, fields=["id", "first_name", "last_name", "email", "role", "image_url"])
            data["image_url"] = user.image_url
            list_data.append(data)
        return list_data
       

    


class Datasets(models.Model):

    status_choices = (

        ("pending", "pending"),
        ("further_review", "further_review"),
        ("published", "published"),
        ("rejected", "rejected"),
    )



    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    published_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="publisher")
    title = models.CharField(max_length=650)
    slug = models.SlugField(max_length=650, null=True)
    license = models.CharField(max_length=650)
    description = models.TextField()
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name="category_datasets", null=True)
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

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)

        super(Datasets, self).save(*args, **kwargs)


    def __str__(self):
        return f"{self.title} -- {self.status} -- {self.published_by.email}"
    
    def delete(self):
        self.is_deleted = True
        self.save()

    
    @property
    def tags_data(self):
        return [model_to_dict(tag, fields=["id", "name"]) for tag in self.tags.all()]
    
    @property
    def organisation_data(self):
        if self.organisation:
            return model_to_dict(self.organisation, fields=["id", "name", "description", "users_data"])
        return None
    
    @property
    def views(self):
        from .models import DatasetViews
        data = DatasetViews.objects.filter(dataset=self)
        if data:
            view = data.first()
            return model_to_dict(view, fields=["count", "created_at", "updated_at"])
        
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
        
    


class DatasetFiles(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dataset = models.ForeignKey(Datasets, on_delete=models.CASCADE, related_name="dataset_files")
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_dataset_files")
    file = models.FileField(upload_to="dataset_files/")
    format = models.CharField(max_length=100)
    size = models.CharField(max_length=100)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.dataset.title} -- {self.format} -- {self.size}"
    
    def delete(self):
        self.is_deleted = True
        self.save()

    @property
    def file_url(self):
        return self.file.url
    
    @property
    def uploader_data(self):
        return model_to_dict(self.uploaded_by, fields=["id", "first_name", "last_name", "email", "role", "image_url"])
    
    @property
    def dataset_data(self):
        return model_to_dict(self.dataset, fields=["id", "title", "image", "organisation_data", "status"])
    





class DatasetViews(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dataset = models.OneToOneField(Datasets, on_delete=models.CASCADE, related_name="dataset_views")
    count = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.dataset.title}"
    
    def delete(self):
        self.is_deleted = True
        self.save()
    
    @property
    def dataset_data(self):
        return model_to_dict(self.dataset, fields=["title", "status", "publisher_data", "organisation_data", "category"])