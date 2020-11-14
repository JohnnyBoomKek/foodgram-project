"""
Dockstrings are very important for both the author of the project and anybody
who ever gets a chance to read the code.
"""
import json

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.contrib import messages


from .models import Recipe, Ingredient, RecipeIngredient, Tag, User, Purchase, Follow
from .forms import RecipeForm

# pdf generator modules
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

def get_tag_url(tags, tag):
    tags_local = tags.copy()
    if tag in tags:
        tags_local.remove(tag)
    else:
        tags_local.append(tag)
    return ",".join(tags_local)


def index(request):
    tags = request.GET.get('tags')
    if tags is None:
        tags = ['B', 'L', 'D']
    else:
        tags = tags.split(',')
    tag_urls = {}
    for tag in ['B', 'L', 'D']:
        tag_urls[tag] = get_tag_url(tags, tag)
    list_of_tags = Tag.objects.filter(tag_name__in=tags)
    recipe_list = Recipe.objects.all().order_by(
        "-pub_date").distinct().filter(tags__in=list_of_tags)
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'page': page,
        'paginator': paginator,
        'tags':tags,
        'tag_urls':tag_urls
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
            ingredients.append([request.POST.get(
                f'nameIngredient_{i}'), request.POST.get(f'valueIngredient_{i}')])
            i += 1
        if form.is_valid():
            new_recipe = form.save(commit=False)
            new_recipe.author = request.user
            new_recipe = form.save()
            ingredients_dict = {}
            for pair in ingredients:
                name = str(pair[0])
                val = int(pair[1])
                if name not in ingredients_dict:
                    ingredients_dict[name] = val
                else:
                    ingredients_dict[name] += val
            for ingredient in ingredients_dict.keys():
                if Ingredient.objects.filter(title=ingredient).exists():
                    RecipeIngredient.objects.create(recipe=new_recipe, ingredient=Ingredient.objects.get(
                    title=ingredient), quantity=ingredients_dict[ingredient])
                else:
                    messages.error(request, f"{ingredient} нету в базе. сорян. попробуй еще раз.")
                    form = RecipeForm(data=request.POST, instance=new_recipe)
                    context = {'recipe': new_recipe,
                                'form': form}
                    return render(request, 'new_recipe.html', context)
            return redirect('index')
    context = {'form': form}
    return render(request, 'new_recipe.html', context)

@login_required
def ingredients(request):
    keyword = request.GET.get('query')
    if keyword:
        ingredient_list = Ingredient.objects.filter(
            title__contains=keyword).values_list()
        data_noice = [{'title': x[1], 'dimension': x[2]}
                      for x in ingredient_list]
        return JsonResponse(data_noice, safe=False)
    else:
        ingredient_list = None
        return JsonResponse({'Found': "None"})

@login_required
def edit_recipe(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    if recipe.author != request.user:
        return HttpResponse('you cannot do it')
    if request.method != 'POST':
        form = RecipeForm(instance=recipe)
    else:
        form = RecipeForm(request.POST or None,
                          files=request.FILES or None, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('single_recipe', slug)
    context = {'recipe': recipe, 'form': form}
    return render(request, 'edit_recipe.html', context)


def single_recipe_view(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    ingredients = recipe.ingredients.all()
    context = {
        'recipe': recipe,
        'ingredients': ingredients
    }
    return render(request, 'detail.html', context)


@login_required
def add_favorites(request):
    data = json.loads(request.body)
    recipe = Recipe.objects.get(id=data["id"])
    recipe.favorite.add(request.user)
    return JsonResponse({'id': request.POST.get('id')})


@login_required
def remove_favorites(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    user = request.user
    user.favorite.remove(recipe)
    return JsonResponse({'id': id})


@login_required
def view_favorites(request, tags=['B','L','D']):
    tags = get_tags(request, tags)
    user = request.user
    recipe_list = user.favorite.all().filter(tags__in=tags[0]).distinct().order_by(
        "-pub_date")
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'page': page,
        'paginator': paginator,
        'user': user,
        'tags':tags[1]
    }
    return render(request, 'index.html', context)


@login_required
def user_recipe(request, username, tags=['B','L','D']):
    #tags = get_tags(request, tags)
    user = get_object_or_404(User, username=username)
    following = Follow.objects.filter(user=request.user).filter(author=user)
    recipe_list = Recipe.objects.filter(tags__in=tags[0]).distinct().filter(
        author=user).order_by('-pub_date')
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'page': page,
        'paginator': paginator,
        'user': user,
        'following': following,
        'tags':tags[1]
    }
    return render(request, 'user_recipes.html', context)


@login_required
def add_purchase(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        recipe = Recipe.objects.get(id=data['id'])
        if not Purchase.objects.filter(user=request.user, recipe=recipe).exists():
            Purchase.objects.create(user=request.user, recipe=recipe)
    return JsonResponse({'Success': True})


@login_required
def remove_purchase(request, id):
    if request.method == 'DELETE':
        user = request.user
        recipe = get_object_or_404(Recipe, id=id)
        purchase = get_object_or_404(Purchase, user=user, recipe=recipe)
        purchase.delete()
        return JsonResponse({'all': 'done'})
    elif request.method == 'GET':
        user = request.user
        recipe = get_object_or_404(Recipe, id=id)
        purchase = get_object_or_404(Purchase, user=user, recipe=recipe)
        purchase.delete()
        return redirect('shopping_list')


@login_required
def shopping_list(request):
    user = request.user
    return render(request, 'shopping_list.html')


@login_required
def download_shopping_list(request):
    purchases = Purchase.objects.filter(user=request.user).values()
    dict_to_print = {}
    for purchase in purchases:
        recipe = get_object_or_404(Recipe, id=purchase['recipe_id'])
        for i in recipe.ingredient_quantity.all():
            if i.ingredient.title not in dict_to_print:
                dict_to_print[i.ingredient.title] = [
                    int(i.quantity), i.ingredient.dimension]
            else:
                dict_to_print[i.ingredient.title][0] += int(i.quantity)
    if not purchases.exists():
        # TODO dobavit' redirect na legit error page
        return HttpResponse('nothing is added to your shopping cart')
    else:
        # pdf generator setup
        pdfmetrics.registerFont(TTFont('Font', 'font.ttf'))
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)
        p.setFont('Font', 32)
        canvas_x = 50
        canvas_y = 740
        step_down = 20
        p.drawString(150, 800, "Список Покупок.")
        p.setFont('Font', 20)
        for i in dict_to_print.keys():
            title = i
            quantity = str(dict_to_print[i][0])
            dimension = dict_to_print[i][1]
            p.drawString(canvas_x, canvas_y, title +
                         "   "+quantity+"   "+dimension)
            canvas_y -= step_down
            if canvas_y < 50 and canvas_x < 400:
                canvas_y = 740
                canvas_x = 400

        p.showPage()
        p.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='hello.pdf')


@login_required
def profile_follow(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        profile = get_object_or_404(User, id=data['id'])
        following = Follow.objects.filter(
            user=request.user).filter(author=profile)
        if request.user != profile:
            if not following:
                Follow.objects.create(user=request.user, author=profile)
                return JsonResponse({'success': True})
            elif following:
                return redirect('index')
        else:
            return redirect('index')


@login_required
def profile_unfollow(request, id):
    if request.method == 'DELETE':
        profile = get_object_or_404(User, id=id)
        if profile == request.user:
            return redirect('index')
        unfollow = Follow.objects.get(user=request.user, author=profile)
        unfollow.delete()
    return JsonResponse({'success': True})


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
