import os
import django
from django.core.files import File

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'thesecretgarden.settings')  # Replace with your settings module
django.setup()

from cloudinary_storage.storage import MediaCloudinaryStorage

try:
    # Initialize Cloudinary storage
    storage = MediaCloudinaryStorage()

    # Provide a valid image file path
    image_path = 'C:/Users/nalan/Downloads/gifts_image_12.jpg'  # Replace with an actual path to an image file on your system

    with open(image_path, 'rb') as image_file:
        django_file = File(image_file)
        # Save file to Cloudinary
        path = storage.save('test_upload/test_image.jpg', django_file)

    print(f"Uploaded file is available at: {path}")

except Exception as e:
    print(f"An error occurred: {e}")
