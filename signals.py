from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

from userprofile.models import UserProfile



def create_profile(sender, **kw):
    user = kw["instance"]
    if kw["created"]:
        up, flag = UserProfile.objects.get_or_create(user=user)
        up.save()
post_save.connect(create_profile, sender=User)
