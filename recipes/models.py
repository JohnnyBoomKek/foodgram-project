from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.

# class Ingredient(models.Model):
#     title = models.CharField(max_length=30)
#     text = models.TextField()

#     def __str__(self):
#         return self.title


class Recipe(models.Model):
    TAG_CHOICES = (
        ('B', 'Breakfast'),
        ('L', 'Lunch'),
        ('D', 'Dinner')
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='recipes/imgs/', blank=True, null=True)
    description = models.TextField()
    tag = models.CharField(max_length=1, choices=TAG_CHOICES)
    cooking_time = models.IntegerField()
    slug = models.SlugField(max_length=140, unique=True)
    pub_date = models.DateTimeField(
        "date published", auto_now_add=True, db_index=True)

    def __str__(self):
        return self.title
