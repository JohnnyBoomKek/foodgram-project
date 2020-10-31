from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Ingredient(models.Model):
    title = models.CharField(max_length=50)
    measurement_unit = models.CharField(max_length=10)

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        'Recipe', related_name='ingredient_quantity', on_delete=models.CASCADE)
    ingredient = models.ForeignKey('Ingredient', on_delete=models.CASCADE)
    quantity = models.CharField(max_length=200)


class Tag(models.Model):
    TAG_CHOICES = (
        ('B', 'Breakfast'),
        ('L', 'Lunch'),
        ('D', 'Dinner')
    )
    tag = models.CharField(max_length=1, choices=TAG_CHOICES)
    recipe = models.ForeignKey(
        "Recipe", on_delete=models.CASCADE, related_name='tag')


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)
    description = models.TextField()
    cooking_time = models.IntegerField()
    slug = models.SlugField(max_length=140, unique=True)
    pub_date = models.DateTimeField(
        "date published", auto_now_add=True, db_index=True)
    ingredients = models.ManyToManyField(Ingredient, through=RecipeIngredient)

    def __str__(self):
        return self.title
