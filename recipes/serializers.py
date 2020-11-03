from .models import Ingredient
from rest_framework import serializers


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("title","dimension")
        model = Ingredient
        