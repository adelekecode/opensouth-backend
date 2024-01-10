import random
from django.dispatch import receiver
from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_save
from django.contrib.auth import get_user_model
from config import settings
from djoser.signals import user_registered, user_activated
from .email import *
from .helpers import *

from django.utils import timezone
from .models import *





@receiver(post_save, sender=Organisations)
def organisation_created_mail(sender, instance, created, **kwargs):

    if created:
        
        pin = generate_organisation_pin(organisation=instance)

        organisation_verification_email(email=instance.email, user=instance.user, organization=instance, pin=pin)


        return

