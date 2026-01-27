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
    file_path = Path(csv_path)                  #file path + existing check / if error raise FileNotFoundError
    if not file_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")          #is handeled in main.py

    df = pd.read_csv(file_path)

    # --- Pandas data cleaning & normalization ---
    df = df.replace("", pd.NA)          #If a cell is empty like "", pandas treats it as missing (NA)

    df = df.dropna(subset=["name", "category", "price", "cooking_time"])            #Remove rows with missing required fields
#cleans data types and formats
    df["name"] = df["name"].astype(str).str.strip()             #astype str ensures value is treated as a string / strip removes leading/trailing spaces
    df["category"] = df["category"].astype(str).str.strip().str.lower()         #stip + lowercase for consistent category names
# Convert price (supports comma decimals)
    df["price"] = (
        df["price"]
        .astype(str)    #strip data type to string
        .str.replace(",", ".", regex=False) #replace comma with dot for decimal
        .astype(float)  #convert to float (decimal number)
    )

    df["cooking_time"] = df["cooking_time"].astype(int)   #convert to integer

    # Remove duplicate recipes by name (keep first)
    df = df.drop_duplicates(subset=["name"])

    # Required columns (keep rating optional for backward compatibility)
    required = ["name", "category", "price", "cooking_time", "ingredients", "steps"]
    for col in required:
        if col not in df.columns:
            raise KeyError(f"Missing required column '{col}' in CSV: {csv_path}")

    has_rating = "rating" in df.columns  # optional

    for row_number, row in enumerate(df.to_dict(orient="records"), start=2):    #convert each the cleaned DataFrame into a list of dictionaries/ start with 2 (header is row 1 in CSV)
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

            # fallback import so the file works both when running from the project root & when running from the src package structure
            try:
                from main import Recipe #
            except ImportError:
                from src.main import Recipe

#Create and add the recipe
            recipe = Recipe(name, category, price, cooking_time, ingredients, steps, rating=rating)
            user.add_recipe(recipe)
# error per row to not skip the whole file
        except (ValueError, KeyError, TypeError) as e:
            print(f"Warning: Invalid data in row {row_number}. Skipping. Error: {e}")
            continue

#Exports current in memory recipes to csv file 
def save_user_recipes_to_csv(user, csv_path: str) -> None:
    """
    Save the user's recipes to a CSV file.

    Columns:
    name,category,price,cooking_time,ingredients,steps,rating
    """
    file_path = Path(csv_path)

    with file_path.open(mode="w", encoding="utf-8", newline="") as file:    
        fieldnames = ["name", "category", "price", "cooking_time", "ingredients", "steps", "rating"]    #defines csv structure
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for recipe in user.recipes:
            writer.writerow({                       # writes each recipe as a row in the csv
                "name": recipe.name,
                "category": recipe.category,
                "price": recipe.price,
                "cooking_time": recipe.cooking_time,
                "ingredients": ";".join(recipe.ingredients),
                "steps": ";".join(recipe.steps),
                "rating": recipe.rating,  # persist ratings
            })

# Import additional recipes from CSV into existing user 
def import_recipes_into_user(user, csv_path: str, dedupe_by_name: bool = True):
    """
    Import recipes from an additional CSV file during runtime.
    Returns: (added_count, skipped_count)
    """
    # Robust import for User    Same reason as Recipe import: path differences.
    try:
        from main import User
    except ImportError:
        from src.main import User

    temp_user = User()          # creates a temporary user to load recipes into to keep existing user clean
    load_recipes_into_user(temp_user, csv_path)
# If no deduplication, extend the list
    if not dedupe_by_name:
        user.recipes.extend(temp_user.recipes)
        return len(temp_user.recipes), 0

    existing_names = {r.name.strip().lower() for r in user.recipes}     ## Create a set with all existing recipe names (lowercase, no spaces)
    added = 0       # Counter: how many new recipes are successfully added
    skipped = 0     #Counter: how many recipes are skipped because they already exist

    for recipe in temp_user.recipes:            #for loop to check each recipe
        key = recipe.name.strip().lower()       # make all names lowercase and strip spaces for comparison
        if key in existing_names:               # check if recipe already exists   
            skipped += 1                         # if exists, increase skipped counter and skip to next recipe 
            continue                            #continou to next recipe
        user.recipes.append(recipe)     #add recipe to main list
        existing_names.add(key)
        added += 1

    return added, skipped           #return how many recipes were added and how many were skipped
