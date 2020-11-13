import csv 
from  recipes.models  import Ingredient, Tag

with open('./recipes/ingredients.csv', newline='', encoding='utf-8') as File:
    reader = csv.reader(File)
    for row in reader:
        ingred = Ingredient(title=row[0], dimension=row[1])
        ingred.save()

tags = ['B', 'L', 'D']
for tag in tags:
    new_tag = Tag(tag_name=tag)
    new_tag.save()
