from django import forms
from django.db import models

from .models import Recipe, Ingredient, RecipeIngredient

class RecipeForm(forms.ModelForm):
    ingredients = forms.CharField(max_length=10)
    class Meta:
        model = Recipe
        fields = ['title',  'ingredients', 'image']

