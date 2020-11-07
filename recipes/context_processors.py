from .models import Purchase


def add_variable_to_context(request):
    if request.user.is_authenticated:
        purchases = Purchase.objects.filter(user=request.user)
    else:
        purchases = None
    return {
        'purchases' : purchases
    }