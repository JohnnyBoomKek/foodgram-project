from django import forms
from django.db import models

from .models import Recipe, Ingredient, RecipeIngredient, Tag

class RecipeForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), required=True, widget=forms.CheckboxSelectMultiple)
    nameINgredient = forms.CharField(required=False)
    valueIngredient = forms.IntegerField(required=False)

    class Meta:
        model = Recipe
        fields = ['title', 'tags', 'cooking_time', 'description', 'image']
        exclude = ('author', 'pub_date', 'ingredients')

        