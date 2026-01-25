# src/io_csv.py
# CSV file handling for Recipe Selection System

import csv
from pathlib import Path
import pandas as pd


def load_recipes_into_user(user, csv_path: str) -> None:
    """
    Load recipes from CSV file into user's recipe list (using pandas).
    Required columns: name, category, price, cooking_time, ingredients, steps
    Optional column: rating
    """
    file_path = Path(csv_path)
    if not file_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    df = pd.read_csv(file_path)

    # --- Pandas data cleaning & normalization ---
    df = df.replace("", pd.NA)

    df = df.dropna(subset=["name", "category", "price", "cooking_time"])

    df["name"] = df["name"].astype(str).str.strip()
    df["category"] = df["category"].astype(str).str.strip().str.lower()

    df["price"] = (
        df["price"]
        .astype(str)
        .str.replace(",", ".", regex=False)
        .astype(float)
    )

    df["cooking_time"] = df["cooking_time"].astype(int)

    # Remove duplicate recipes by name (keep first)
    df = df.drop_duplicates(subset=["name"])
    # ------------------------------------------

    # Required columns (keep rating optional for backward compatibility)
    required = ["name", "category", "price", "cooking_time", "ingredients", "steps"]
    for col in required:
        if col not in df.columns:
            raise KeyError(f"Missing required column '{col}' in CSV: {csv_path}")

    has_rating = "rating" in df.columns  # optional

    for row_number, row in enumerate(df.to_dict(orient="records"), start=2):
        try:
            name = str(row["name"]).strip()
            category = str(row["category"]).strip()

            # Convert price (supports comma decimals)
            price_str = str(row["price"]).strip().replace(",", ".")
            price = float(price_str)

            # Convert cooking time
            cooking_time = int(str(row["cooking_time"]).strip())

            # Split ingredients / steps by ';'
            ingredients = [x.strip() for x in str(row["ingredients"]).split(";") if x.strip()]
            steps = [x.strip() for x in str(row["steps"]).split(";") if x.strip()]

            # Optional rating (default 0.0 if missing/empty)
            rating = 0.0
            if has_rating:
                rating_str = str(row["rating"]).strip().replace(",", ".")
                rating = float(rating_str) if rating_str else 0.0

            # Local import to keep current setup (robust)
            try:
                from main import Recipe
            except ImportError:
                from src.main import Recipe

            recipe = Recipe(name, category, price, cooking_time, ingredients, steps, rating=rating)
            user.add_recipe(recipe)

        except (ValueError, KeyError, TypeError) as e:
            print(f"Warning: Invalid data in row {row_number}. Skipping. Error: {e}")
            continue


def save_user_recipes_to_csv(user, csv_path: str) -> None:
    """
    Save the user's recipes to a CSV file.

    Columns:
    name,category,price,cooking_time,ingredients,steps,rating
    """
    file_path = Path(csv_path)

    with file_path.open(mode="w", encoding="utf-8", newline="") as file:
        fieldnames = ["name", "category", "price", "cooking_time", "ingredients", "steps", "rating"]
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
                "rating": recipe.rating,  # persist ratings
            })


def import_recipes_into_user(user, csv_path: str, dedupe_by_name: bool = True):
    """
    Import recipes from an additional CSV file during runtime.
    Returns: (added_count, skipped_count)
    """
    # Robust import for User (same idea as Recipe)
    try:
        from main import User
    except ImportError:
        from src.main import User

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
