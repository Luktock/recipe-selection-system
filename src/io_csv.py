# src/io_csv.py
# CSV file handling for Recipe Selection System

import csv
from pathlib import Path
import pandas as pd


def load_recipes_into_user(user, csv_path: str) -> None:
    """
    Load recipes from CSV file into user's recipe list (using pandas).
    Each row must contain: name, category, price, cooking_time, ingredients, steps
    """
    file_path = Path(csv_path)
    if not file_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    # Read CSV with pandas
    df = pd.read_csv(file_path)

    # Basic validation: required columns
    required = ["name", "category", "price", "cooking_time", "ingredients", "steps"]
    for col in required:
        if col not in df.columns:
            raise KeyError(f"Missing required column '{col}' in CSV: {csv_path}")

    # Iterate rows as dictionaries (simple)
    for row_number, row in enumerate(df.to_dict(orient="records"), start=2):
        try:
            name = str(row["name"]).strip()
            category = str(row["category"]).strip()

            # Convert price (also supports comma decimal)
            price_str = str(row["price"]).strip().replace(",", ".")
            price = float(price_str)

            # Convert cooking time
            cooking_time = int(str(row["cooking_time"]).strip())

            # Ingredients / steps split by ';' (remove empty entries)
            ingredients = [x.strip() for x in str(row["ingredients"]).split(";") if x.strip()]
            steps = [x.strip() for x in str(row["steps"]).split(";") if x.strip()]

            # Import Recipe class here to avoid circular imports (keep your current setup)
            from main import Recipe

            recipe = Recipe(name, category, price, cooking_time, ingredients, steps)
            user.add_recipe(recipe)

        except (ValueError, KeyError, TypeError) as e:
            print(f"Warning: Invalid data in row {row_number}. Skipping. Error: {e}")
            continue


def save_user_recipes_to_csv(user, csv_path: str) -> None:
    """
    Save the user's recipes to a CSV file.

    CSV columns:
    name,category,price,cooking_time,ingredients,steps
    """
    file_path = Path(csv_path)

    with file_path.open(mode="w", encoding="utf-8", newline="") as file:
        fieldnames = ["name", "category", "price", "cooking_time", "ingredients", "steps"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for recipe in user.recipes:
            writer.writerow({
                "name": recipe.name,
                "category": recipe.category,
                "price": recipe.price,
                "cooking_time": recipe.cooking_time,
                "ingredients": ";".join(recipe.ingredients),
                "steps": ";".join(recipe.steps),
            })


def import_recipes_into_user(user, csv_path: str, dedupe_by_name: bool = True):
    """
    Import recipes from an additional CSV file during runtime.
    Recipes are appended to the existing user.recipes list.

    Returns:
        (added_count, skipped_count)
    """
    # Keep your current approach (simple + works)
    from main import User

    temp_user = User()
    load_recipes_into_user(temp_user, csv_path)

    if not dedupe_by_name:
        user.recipes.extend(temp_user.recipes)
        return len(temp_user.recipes), 0

    existing_names = {r.name.strip().lower() for r in user.recipes}
    added = 0
    skipped = 0

    for recipe in temp_user.recipes:
        key = recipe.name.strip().lower()
        if key in existing_names:
            skipped += 1
            continue
        user.recipes.append(recipe)
        existing_names.add(key)
        added += 1

    return added, skipped
