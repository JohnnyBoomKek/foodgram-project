from .models import Purchase, Tag, Recipe
from django.core.paginator import Paginator


def add_variable_to_context(request):
    if request.user.is_authenticated:
        purchases = Purchase.objects.filter(user=request.user)
        recipe_purchase = []
        for i in purchases:
            recipe_purchase.append(i.recipe.id)
    else:
        purchases = None
        recipe_purchase = None
    context = {
        'purchases' : purchases,
        "recipe_purchase":recipe_purchase
    }
    return context
