from django.contrib import admin

# Register your models here.
from .models import Recipe, Ingredient, RecipeIngredient, Tag


admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(RecipeIngredient)
admin.site.register(Tag)