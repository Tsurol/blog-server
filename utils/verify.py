def current_user(request):
    if not request.user.is_active:
        return None
    return request.user
