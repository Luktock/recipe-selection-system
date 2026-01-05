import pandas as pd
import time


def load_recipes():
    file_path = "data/recipes.csv"
    recipes = pd.read_csv(file_path)
    return recipes


def show_recipe_details(recipes):
    recipe_id = input("Enter recipe ID: ")

    if not recipe_id.isdigit():
        print("Invalid ID.")
        return

    recipe_id = int(recipe_id)
    recipe = recipes[recipes["id"] == recipe_id]

    if recipe.empty:
        print("Recipe not found.")
        return

    recipe = recipe.iloc[0]

    print("\nRecipe Details")
    print(f"Name: {recipe['name']}")
    print(f"Category: {recipe['category']}")
    print(f"Price: €{recipe['price']}")
    print(f"Cooking time: {recipe['time_min']} minutes")
    print(f"Ingredients: {recipe['ingredients']}")
    print(f"Steps: {recipe['steps']}")


def run_performance_test(recipes):
    print("\nRunning performance test...")

    start_time = time.time()

    for _ in range(10000):
        _ = recipes.copy()

    end_time = time.time()

    print(f"Time taken: {end_time - start_time:.4f} seconds")


def save_recipes(recipes):
    file_path = "data/recipes_updated.csv"
    recipes.to_csv(file_path, index=False)
    print(f"Saved to {file_path}")


def main():
    recipes = load_recipes()
    print("Welcome to the Recipe Selection System!")
    print(f"Number of recipes loaded: {len(recipes)}")

    while True:
