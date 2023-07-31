def add_slug_to_context(request):
    if hasattr(request, 'user') and request.user.is_authenticated:
        return {'slug': request.user.profile.slug if hasattr(request.user, 'profile') else None}
    return {}