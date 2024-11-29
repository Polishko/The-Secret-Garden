from django.db.models.signals import post_delete
from django.dispatch import receiver
from thesecretgarden.flowers.models import Plant
from thesecretgarden.gifts.models import Gift

@receiver(post_delete, sender=Plant)
def delete_plant_photo(sender, instance, **kwargs):
    if instance.photo and instance.photo.storage.exists(instance.photo.name):
        if instance.photo:
            instance.photo.delete(save=False)

@receiver(post_delete, sender=Gift)
def delete_gift_photo(sender, instance, **kwargs):
    if instance.photo and instance.photo.storage.exists(instance.photo.name):
        if instance.photo:
            instance.photo.delete(save=False)
