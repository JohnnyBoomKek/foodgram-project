from django import forms
from django.db import models

from .models import Recipe, Ingredient, RecipeIngredient, Tag

class RecipeForm(forms.ModelForm):
    tag_choice = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)
    nameINgredient = forms.CharField(required=False)
    valueIngredient = forms.IntegerField(required=False)

    class Meta:
        model = Recipe
        fields = ['title', 'tag_choice', 'cooking_time', 'description', 'image']
        exclude = ('author', 'pub_date', 'tag', 'ingredients')

