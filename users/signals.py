

from django.contrib.auth.models import User
from django.db.models.fields.related import ForeignKey
from django.db.models.signals import post_delete, post_save
from .models import Profile

# @receiver(post_save, sender=Profile)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user, 
            username=user.username,
            email=user.email,
            name=user.first_name
        )

# @receiver(post_save, sender=Profile)
def delete_profile(sender, instance, **kwargs):
    user = instance.user
    print("useruseruseruseruseruser--> ", user)
    user.delete()
    print("Profile deleted--> ", instance)

# Everytime a user is created a profile will be created as well
post_save.connect(create_profile, sender=User)
post_delete.connect(delete_profile, sender=Profile)
