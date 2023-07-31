from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal receiver function to create a Profile instance when a new User is created.

    Args:
        sender: The model class that sends the signal.
        instance: The User instance being saved.
        created: A boolean indicating if the User instance was newly created.
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Signal receiver function to save the Profile instance when the associated User is saved.

    Args:
        sender: The model class that sends the signal.
        instance: The User instance being saved.
    """
    instance.profile.save()
