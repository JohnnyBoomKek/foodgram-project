from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core import serializers

import json

from .models import Recipe, Ingredient, RecipeIngredient, Tag
from .forms import RecipeForm
from .serializers import IngredientSerializer
# Create your views here.

tags = ['B', 'L', 'D']

def index(request):
    tag = request.GET.get('tags')
    if tag is not None:
        if tag not in tags:
            tags.append(tag)
        else:
            tags.remove(tag)
    
    list_of_tags = Tag.objects.filter(tag_name__in=tags)
    print(list_of_tags)
    recipe_list = Recipe.objects.filter(tags__in=list_of_tags).distinct().order_by("-pub_date")
    veslist = Recipe.objects.all()
    #print([x.tags for x in recipe_list])
    #print(veslist)
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'page': page,
        'paginator': paginator,
        'tags': tags
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
        if form.is_valid():
            new_recipe = form.save(commit=False)
            new_recipe.author = request.user
            new_recipe = form.save()
            ingredients_dict = {}
            for pair in ingredients:
                name = str(pair[0])
                val  = int(pair[1])
                if name not in ingredients_dict:
                    ingredients_dict[name]=val
                else:
                    ingredients_dict[name]+=val
            for ingredient in ingredients_dict.keys():
                RecipeIngredient.objects.create(recipe=new_recipe, ingredient = Ingredient.objects.get(title=ingredient), quantity = ingredients_dict[ingredient])
            selected_tags = request.POST.getlist('tag_choice')
            for tag in selected_tags:
                new_recipe.tags.add(tag)
            return redirect('index')
    context = {'form': form}
    return render(request, 'new_recipe.html', context)

def ingredients(request):
    keyword = request.GET.get('query')
    if keyword:
        ingredient_list = Ingredient.objects.filter(title__contains=keyword)
        data_noice = [{"title": x.title, "dimension":x.dimension} for x in ingredient_list]
        return  JsonResponse(data_noice, safe=False)
    else:
        ingredient_list = None
    

def single_recipe_view(request, slug):
     recipe = get_object_or_404(Recipe, slug=slug)
     ingredients = recipe.ingredients.all()
     context = {
         'recipe':recipe,
         'ingredients':ingredients
     }
     return render(request, 'detail.html', context)

def add_favorites(request):
    data = json.loads(request.body)
    recipe = Recipe.objects.get(id = data["id"])
    recipe.favorite.add(request.user)
    return JsonResponse({'id':request.POST.get('id')})

def remove_favorites(request, id):
    recipe = Recipe.objects.get(id=id)
    user = request.user
    user.favorite.remove(recipe)
    return JsonResponse({'isd':id})

def view_favorites(request):
    tag = request.GET.get('tags')
    if tag is not None:
        if tag not in tags:
            tags.append(tag)
        else:
            tags.remove(tag)
    list_of_tags = Tag.objects.filter(tag_name__in=tags)
    user = request.user
    recipe_list = user.favorite.all().order_by("-pub_date").filter(tags__in=list_of_tags)
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'page': page,
        'paginator': paginator,
        'tags': tags, 
        'user': user
    }
    return render(request, 'index.html', context)