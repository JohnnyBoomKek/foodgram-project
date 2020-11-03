from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Ingredient(models.Model):
    title = models.CharField(max_length=50)
    dimension = models.CharField(max_length=10)
    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        'Recipe', related_name='ingredient_quantity', on_delete=models.CASCADE)
    ingredient = models.ForeignKey('Ingredient', on_delete=models.CASCADE)
    quantity = models.CharField(max_length=200)

    def __str__(self):
        return self.recipe.title


class Tag(models.Model):
    TAG_CHOICES = (
        ('B', 'Breakfast'),
        ('L', 'Lunch'),
        ('D', 'Dinner')
    )
    tag_name = models.CharField(max_length=1, choices=TAG_CHOICES)

    def __str__(self):
        return self.tag_name


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)
    description = models.TextField()
    cooking_time = models.IntegerField()
    #slug = models.SlugField(max_length=140, unique=True)
    pub_date = models.DateTimeField(
        "date published", auto_now_add=True, db_index=True)
    ingredients = models.ManyToManyField(Ingredient, through=RecipeIngredient)
    tags = models.ManyToManyField(Tag)
    favorite = models.ManyToManyField(User, related_name='favorite', blank=True)

    def __str__(self):
        return self.title
