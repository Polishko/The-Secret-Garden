from django.db.models.signals import post_delete
from django.dispatch import receiver
from cloudinary import api
from thesecretgarden.flowers.models import Plant
from thesecretgarden.gifts.models import Gift


@receiver(post_delete, sender=Plant)
def delete_plant_photo(sender, instance, **kwargs):
    # print("Signal Triggered: Deleting Plant Photo")
    if instance.photo:
        try:
            public_id = instance.photo
            # print("Deleting from Cloudinary:", public_id)
            api.delete_resources([public_id])  # Delete the resource from Cloudinary
        except Exception as e:
            print(f"Error deleting photo: {e}")

@receiver(post_delete, sender=Gift)
def delete_gift_photo(sender, instance, **kwargs):
    # print("Signal Triggered: Deleting Gift Photo")
    if instance.photo:
        try:
            public_id = instance.photo
            # print("Deleting from Cloudinary:", public_id)
            api.delete_resources([public_id])  # Delete the resource from Cloudinary
        except Exception as e:
            print(f"Error deleting photo: {e}")
