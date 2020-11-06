from django.urls import include, path
from . import views 

urlpatterns = [
    path('', views.index, name = "index"), 
    path('new/', views.new, name='new'),
    path('ingredients', views.ingredients, name='ingredients'),
    path('recipe/<str:slug>', views.single_recipe_view, name='single_recipe'), 
    path('favorites', views.add_favorites, name='add_favorite'), 
    path('favorites/<int:id>', views.remove_favorites, name='remove_favorite'),
    path('favorite_recepies', views.view_favorites, name='view_favorites'),  
    
]
