from rest_framework import serializers

from thesecretgarden.common.models import ContactMessage


class ContactMessageSerializer(serializers.ModelSerializer):
    """Serializer for validating and saving contact messages."""
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
