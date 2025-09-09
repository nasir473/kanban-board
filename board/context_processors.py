from .models import Space


def spaces_processor(request):
    """Provide a list of space names and current workspace to all templates."""
    spaces_qs = Space.objects.all().order_by('name')
    spaces = [s.name for s in spaces_qs]
    default_space = spaces[0] if spaces else 'office'
    current_workspace = request.session.get('current_workspace', default_space)
    # If current workspace was deleted, fallback
    if current_workspace not in spaces and spaces:
        current_workspace = spaces[0]
        request.session['current_workspace'] = current_workspace
    return {
        'spaces': spaces,
        'current_workspace': current_workspace,
    }
