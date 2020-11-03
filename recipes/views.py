from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core import serializers


from .models import Recipe, Ingredient, RecipeIngredient
from .forms import RecipeForm
from .serializers import IngredientSerializer
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
        i = 1
        ingredients = []
        while request.POST.get(f'nameIngredient_{i}') is not None:
            ingredients.append([request.POST.get(f'nameIngredient_{i}'), request.POST.get(f'valueIngredient_{i}')])
            i += 1
        print(ingredients)
        if form.is_valid():
            new_recipe = form.save(commit=False)
            new_recipe.author = request.user
            new_recipe = form.save()
            for ingredient in ingredients:
                print('this is k[0]', ingredient[0])
                new_recipe.ingredients.set(Ingredient.objects.filter(title=ingredient[0]))
                RecipeIngredient.objects.create(recipe=new_recipe, ingredient = Ingredient.objects.get(title=ingredient[0]), quantity = ingredient[1])
            return redirect('index')
        else:
            print("Form is not valid", form.non_field_errors )
    context = {'form': form}
    return render(request, 'new_recipe.html', context)

def ingredients(request):
    keyword = request.GET.get('query')
    if keyword:
        ingredient_list = Ingredient.objects.all()
        data_noice = [{"title": x.title, "dimension":x.dimension} for x in ingredient_list]
        return  JsonResponse(data_noice, safe=False)
    else:
        ingredient_list = None
    