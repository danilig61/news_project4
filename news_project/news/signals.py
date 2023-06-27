from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(instance, created):
    if created:
        UserProfile.objects.create(user=instance)
        group = Group.objects.get(name='authors')
        instance.groups.add(group)