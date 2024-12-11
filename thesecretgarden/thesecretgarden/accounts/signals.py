from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_save
from django.dispatch import receiver
from thesecretgarden.accounts.models import Profile
from django.db import transaction


UserModel = get_user_model()


@receiver(post_save, sender=UserModel)
def create_profile(sender, instance, created, **kwargs):
    """
    Automatically creates Profile for a User on instantiation
    """
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
    Udates app user is_active status when user inactivates their profile
    """
    user = instance.user
    if user.is_active != instance.is_active:
        user.is_active = instance.is_active
        user.save()

@receiver(post_save, sender=UserModel)
def add_to_group_based_on_role(sender, instance, created, **kwargs):
    """
    Automatically adds users to the appropriate group based on their role
    and ensures groups have the correct permissions (only for staff).
    """
    def ensure_group_permissions(group_name, permissions):
        """
        Ensures the group has the specified permissions.
        """
        group, _ = Group.objects.get_or_create(name=group_name)
        for codename in permissions:
            try:
                permission = Permission.objects.get(codename=codename)
                group.permissions.add(permission)
            except Permission.DoesNotExist:
                print(f"Permission with codename '{codename}' does not exist.")
        return group

    if created:
        if instance.is_staff:
            # Admin panel permissions for the Staff group
            staff_permissions = [
                'view_orderitem',      # Can view OrderItem
                'view_order',          # Can view Order
                'add_gift',            # Can add Gift
                'change_gift',         # Can change Gift
                'delete_gift',         # Can delete Gift
                'view_gift',           # Can view Gift
                'add_plant',           # Can add Plant
                'change_plant',        # Can change Plant
                'delete_plant',        # Can delete Plant
                'view_plant',          # Can view Plant
                'view_user',           # Can view User
                'view_profile',        # Can view Profile
                'view_contactmessage', # Can view ContactMessage
            ]
            staff_group = ensure_group_permissions('Staff', staff_permissions)
            instance.groups.add(staff_group)
        else:
            customer_group, _ = Group.objects.get_or_create(name='Customer')
            instance.groups.add(customer_group)
