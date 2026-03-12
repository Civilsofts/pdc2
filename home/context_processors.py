from .models import ServiceCategory


def menu_categories(request):
    categories = ServiceCategory.objects.filter(is_active=True).prefetch_related('items')
    return {'menu_categories': categories}
