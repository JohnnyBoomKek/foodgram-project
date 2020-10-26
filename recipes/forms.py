from django import forms
from django.db import models

from .models import Recipe, Ingredient, RecipeIngredient

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'tag', 'ingredients', 'image']
