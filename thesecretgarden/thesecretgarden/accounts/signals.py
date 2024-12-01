from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from thesecretgarden.accounts.models import Profile
from django.db import transaction


UserModel = get_user_model()


@receiver(post_save, sender=UserModel)
def create_profile(sender, instance, created, **kwargs):
    if created:
        with transaction.atomic():
            Profile.objects.create(
                user=instance,
                first_name='Anonymous',
                last_name='User'
            )

@receiver(post_save, sender=Profile)
def sync_user_is_active(sender, instance, **kwargs):
    """
        Signal to update app user is_active status when user inactivates their profile
    """
    user = instance.user
    if user.is_active != instance.is_active:
        user.is_active = instance.is_active
        user.save()


@receiver(post_save, sender=UserModel)
def add_to_group_based_on_role(sender, instance, created, **kwargs):
    """
    Automatically add users to the appropriate group based on their role.
    """
    if created:
        if instance.is_staff:
            # Assign to 'Staff' group
            staff_group, _ = Group.objects.get_or_create(name='Staff')
            instance.groups.add(staff_group)
        else:
            # Assign to 'Customer' group
            customer_group, _ = Group.objects.get_or_create(name='Customer')
            instance.groups.add(customer_group)
