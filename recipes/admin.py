from django.contrib import admin

# Register your models here.
from .models import Recipe, Ingredient, RecipeIngredient, Tag, Purchase


admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(RecipeIngredient)
admin.site.register(Tag)
admin.site.register(Purchase)