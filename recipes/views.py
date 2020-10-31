from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .models import Recipe, Ingredient, RecipeIngredient
from .forms import RecipeForm
# Create your views here.


def index(request):
    recipe_list = Recipe.objects.order_by("-pub_date").all()
    paginator = Paginator(recipe_list, 4)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'page': page,
        'paginator': paginator,
    }
    return render(request, 'index.html', context)

@login_required
def new(request):
    if request.method != 'POST':
        form = RecipeForm()
    else:
        form = RecipeForm(request.POST or None, files=request.FILES or None)
        if form.is_valid():
            new_recipe = form.save(commit=False)
            new_recipe.author = request.user
            new_recipe = form.save()
            return redirect('index')
    context = {'form': form}
    return render(request, 'new_recipe.html', context)

def ingredients(request):
    keyword = request.GET.get('query')
    if keyword:
        ingredient_list = Ingredient.objects.values('title').filter(title__icontains=keyword)
    else:
        ingredient_list = None
    return JsonResponse({"ingredientent_list":list(ingredient_list)})