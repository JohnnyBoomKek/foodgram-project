from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core import serializers

import json

from .models import Recipe, Ingredient, RecipeIngredient, Tag, User, Purchase, Follow
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
    recipe_list = Recipe.objects.filter(tags__in=list_of_tags).distinct().order_by("-pub_date")
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    if request.user.is_authenticated:
        purchases = Purchase.objects.filter(user=request.user)
    else:
        purchases = None
    context = {
        'page': page,
        'paginator': paginator,
        'tags': tags,
        'purchases':purchases
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

@login_required
def edit_recipe(request, slug):
    recipe = Recipe.objects.get(slug=slug)
    if recipe.author != request.user:
        raise Http404
    if request.method != 'POST':
        form = RecipeForm(instance=recipe)
    else:
        form = RecipeForm(request.POST or None,
                        files=request.FILES or None, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('single_recipe', slug)
    context = {'recipe': recipe, 'form': form}
    return render(request, "edit_recipe.html", context)



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

@login_required
def view_favorites(request):
    tag = request.GET.get('tags')
    if tag is not None:
        if tag not in tags:
            tags.append(tag)
        else:
            tags.remove(tag)
    list_of_tags = Tag.objects.filter(tag_name__in=tags)
    user = request.user
    recipe_list = user.favorite.all().order_by("-pub_date").filter(tags__in=list_of_tags).distinct()
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

def user_recipe(request, username):
    tag = request.GET.get('tags')
    if tag is not None:
        if tag not in tags:
            tags.append(tag)
        else:
            tags.remove(tag)
    list_of_tags = Tag.objects.filter(tag_name__in=tags)
    user = get_object_or_404(User, username=username)
    following = Follow.objects.filter(user=request.user).filter(author=user)
    recipe_list = Recipe.objects.filter(tags__in=list_of_tags).distinct().filter(author=user).order_by("-pub_date")
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'page': page,
        'paginator': paginator,
        'tags': tags,
        'user':user,
        'following':following
    }
    return render(request, 'user_recipes.html',context)

@login_required
def add_purchase(request):
    if request.method == "POST":
        data = json.loads(request.body)
        recipe = Recipe.objects.get(id = data["id"])
        if not Purchase.objects.filter(user=request.user, recipe=recipe).exists():
            Purchase.objects.create(user=request.user, recipe=recipe)
    return JsonResponse({'s':"s"})

@login_required
def remove_purchase(request, id):
    if request.method == "DELETE":
        user = request.user
        recipe = get_object_or_404(Recipe, id=id)
        purchase = get_object_or_404(Purchase, user=user, recipe=recipe)
        purchase.delete()
        return JsonResponse({"all":"done"})
    elif request.method == "GET":
        user = request.user
        recipe = get_object_or_404(Recipe, id=id)
        purchase = get_object_or_404(Purchase, user=user, recipe=recipe)
        purchase.delete()
        return redirect('shopping_list')

@login_required
def shopping_list(request):
    user = request.user
    purchases = Purchase.objects.filter(user=user)
    return render(request,'shopping_list.html', {'purchases':purchases})

@login_required
def profile_follow(request):
    if request.method == "POST":
        data = json.loads(request.body)
        profile = get_object_or_404(User, id=data['id'])
        following = Follow.objects.filter(user=request.user).filter(author=profile)
        if request.user != profile:
            if not following:
                Follow.objects.create(user=request.user, author=profile)
                return JsonResponse({'success':True})
            elif following:
                return redirect('index')

@login_required
def profile_unfollow(request, id):
    if request.method == "DELETE":
        profile = get_object_or_404(User, id=id)
        if profile == request.user:
            return redirect('index')
        unfollow = Follow.objects.get(user=request.user, author=profile)
        unfollow.delete()
        print('You are not following this author anymore')
    return JsonResponse({'success':True})
        

@login_required
def subscriptions_view(request):
    following_list = request.user.follower.all()
    paginator = Paginator(following_list, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'page': page,
        'paginator': paginator,
    }
    return render(request, 'subscriptions.html', context)

