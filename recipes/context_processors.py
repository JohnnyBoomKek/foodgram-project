from .models import Purchase, Tag, Recipe
from django.core.paginator import Paginator


def add_variable_to_context(request):
    if request.user.is_authenticated:
        purchases = Purchase.objects.filter(user=request.user)
    else:
        purchases = None
    context = {
        'purchases' : purchases,
    }
    return context
