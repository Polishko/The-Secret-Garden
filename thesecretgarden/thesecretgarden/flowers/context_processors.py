from .models import Plant

def recommended_products(request):
    if request.user.is_authenticated:
        profile = getattr(request.user, 'profile', None)
        if profile and profile.preferred_flower_type:
            print(profile.preferred_flower_type)
            recommended_plants = Plant.objects.filter(
                type=profile.preferred_flower_type
            ).order_by('-created_at')[:5]
            print(f"Recommended Plants: {recommended_plants}")
            return {'recommended_plants': recommended_plants}

    return {}
