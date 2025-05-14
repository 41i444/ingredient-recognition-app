import os
import json
from ultralytics import YOLO
from PIL import Image

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

def recommend_recipes(ingredients, all_recipes):
    recommended = []
    for recipe in all_recipes:
        if any(ing in ingredients for ing in recipe["ingredients"]):
            recommended.append(recipe)
    return recommended[:3]

def get_full_recipe(title):
    path = os.path.join("full_recipes", title.replace(" ", "_").lower())
    instructions_path = os.path.join(path, "instructions.txt")
    image_path = os.path.join(path, "image.jpg")
    
    with open(instructions_path, "r") as f:
        instructions = f.read()
    image = Image.open(image_path)

    return instructions, image

