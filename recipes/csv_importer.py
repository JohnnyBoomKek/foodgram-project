import csv 
from  recipes.models  import Ingredient

with open('./recipes/ingredients.csv', newline='', encoding='utf-8') as File:
    reader = csv.reader(File)
    for row in reader:
        ingred = Ingredient(title=row[0], measurement_unit=row[1])
        ingred.save()