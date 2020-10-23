from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse

from .models import Recipe
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


# def index(request):
#     post_list = Post.objects.order_by("-pub_date").all()
#     # показывать по 10 записей на странице.
#     paginator = Paginator(post_list, 10)
#     # переменная в URL с номером запрошенной страницы
#     page_number = request.GET.get('page')
#     # получить записи с нужным смещением
#     page = paginator.get_page(page_number)
#     return render(request, 'index.html', {'page': page, 'paginator': paginator})
