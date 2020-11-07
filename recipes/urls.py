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
    path('purchases', views.add_purchase, name='add_purchase'),
    path('purchases/<int:id>', views.remove_purchase, name='remove_purchase'),
    path('shopping_list', views.shopping_list, name='shopping_list'),
    path('subscriptions', views.profile_follow, name='follow'),
    path('subscriptions/<int:id>', views.profile_unfollow, name='unfollow'),
    path('subscriptions_index', views.subscriptions_view, name='view_subscriptions'),
    path('<str:username>', views.user_recipe, name='user_recipe'),
    
    
]
