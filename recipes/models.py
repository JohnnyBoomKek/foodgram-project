from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save
from django.template.defaultfilters import slugify


from .utils import unique_slug_generator

User = get_user_model()


class Ingredient(models.Model):
    title = models.CharField(max_length=50)
    dimension = models.CharField(max_length=10)

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        'Recipe', related_name='ingredient_quantity', on_delete=models.CASCADE)
    ingredient = models.ForeignKey(
        'Ingredient', related_name='ingredient', on_delete=models.CASCADE)
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
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipes')
    title = models.CharField(max_length=200)
    image = models.ImageField(
        upload_to='recipes/', blank=True, default='recipes/default.jpg', null=True)
    description = models.TextField()
    cooking_time = models.PositiveIntegerField()
    slug = models.SlugField(max_length=140, unique=True, null=True, blank=True)
    pub_date = models.DateTimeField(
        'date published', auto_now_add=True, db_index=True)
    ingredients = models.ManyToManyField(Ingredient, through=RecipeIngredient)
    tags = models.ManyToManyField(Tag)
    favorite = models.ManyToManyField(
        User, related_name='favorite', blank=True)

    def __str__(self):
        return self.title


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='purchases')

    def __str__(self):
        return self.recipe.title


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower')  # подписчик
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following')  # подписуемый

    def __str__(self):
        return f'follower - {self.user} following - {self.author}'

# unique slug generator related business


def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(pre_save_receiver, sender=Recipe)
