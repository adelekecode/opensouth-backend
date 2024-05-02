from django.db import models
import uuid
from django.contrib.auth import get_user_model
from datetime import datetime

# Create your models here.



User = get_user_model()







class TokenManager(models.Manager):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_token")
    token = models.CharField(max_length=6500)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.user.email
    

    def delete_token(self):

        self.is_deleted = True
        self.is_active = False
        self.token = f"{self.token}--deleted--{datetime.now().date()}"
        self.save()
