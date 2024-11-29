"""
Callable that uploads photo to specific local destination based on product model
"""

def dynamic_upload_to(instance, filename):
    from thesecretgarden.flowers.models import Plant
    from thesecretgarden.gifts.models import Gift
    if isinstance(instance, Plant):
        return f'images/flowers/{filename}'
    elif isinstance(instance, Gift):
        return f'images/gifts/{filename}'
    return f'images/other/{filename}'





