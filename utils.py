import os
import json
from PIL import Image
from ultralytics import YOLO

def load_model(path):
    return YOLO(path)

def predict_ingredients(model, image):
    results = model(image)
    ingredients = list(set([model.names[int(cls)] for cls in results[0].boxes.cls.tolist()]))
    return ingredients

def load_recipes():
    recipes = []
    for file in os.listdir("recipes"):
        with open(os.path.join("recipes", file), "r") as f:
            recipe = json.load(f)
            recipes.append(recipe)
    return recipes

def recommend_recipes(input_ingredients, all_recipes):
    input_set = set(i.lower().strip() for i in input_ingredients)
    recommended = []
    for recipe in all_recipes:
        recipe_ingredients = set(i.lower().strip() for i in recipe['ingredients'])
        if input_set.issubset(recipe_ingredients):
            recommended.append(recipe)
    return recommended[:5]

def get_full_recipe(title):
    path = os.path.join("full_recipes", title.replace(" ", "_").lower())
    instructions_path = os.path.join(path, "instructions.txt")
    image_path = os.path.join(path, "image.jpg")
    
    with open(instructions_path, "r") as f:
        instructions = f.read()
        
    image = Image.open(image_path)

    return instructions, image
