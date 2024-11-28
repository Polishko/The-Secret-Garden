from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from thesecretgarden.accounts.models import Profile


UserModel = get_user_model()

@receiver(post_save, sender=UserModel)
def create_profile(sender, instance, created, **kwargs):
    """
        Signal to create a Profile when a new User is created.
    """
    if created:
        Profile.objects.create(
            user=instance,
            first_name='Anonymous',
            last_name='User'
        )


@receiver(post_save, sender=Profile)
def sync_user_is_active(sender, instance, **kwargs):
    """
        Signal to update app user is_active status when customer inactivates their profile
    """
    user = instance.user
    if user.is_active != instance.is_active:
        user.is_active = instance.is_active
        user.save()
