# src/io_csv.py
# CSV file handling for Recipe Selection System

import csv
from pathlib import Path


def load_recipes_into_user(user, csv_path: str) -> None:
    """
    Load recipes from CSV file into user's recipe list
    
    Args:
        user: User object with add_recipe method
        csv_path: Path to CSV file as string
    
    Raises:
        FileNotFoundError: If CSV file does not exist
    """
    # Convert string path to Path object and check if file exists
    file_path = Path(csv_path)
    if not file_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    
    # Open and read CSV file
    with file_path.open(mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        
        # Process each row (skip header automatically with DictReader)
        for row_number, row in enumerate(csv_reader, start=2):  # Start at 2 (row 1 is header)
            try:
                # Extract and clean data from CSV row
                name = row['name'].strip()
                category = row['category'].strip()
                
                # Convert price (handle comma as decimal separator)
                price_str = row['price'].strip().replace(',', '.')
                price = float(price_str)
                
                # Convert cooking time to integer
                cooking_time = int(row['cooking_time'].strip())
                
                # Split ingredients by semicolon into list
                ingredients_str = row['ingredients'].strip()
                ingredients = [item.strip() for item in ingredients_str.split(';')]
                
                # Split steps by semicolon into list
                steps_str = row['steps'].strip()
                steps = [item.strip() for item in steps_str.split(';')]
                
                # Import Recipe class here to avoid circular imports
                from main import Recipe
                
                # Create Recipe object
                recipe = Recipe(name, category, price, cooking_time, ingredients, steps)
                
                # Add recipe to user
                user.add_recipe(recipe)
                
            except (ValueError, KeyError) as e:
                # Print warning and continue with next row
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

#-----------------Import newrecipesfromadditionalCSVfiles--------------

def import_recipes_into_user(user, csv_path: str, dedupe_by_name: bool = True):
    """
    Import recipes from an additional CSV file during runtime.
    Recipes are appended to the existing user.recipes list.

    Args:
        user: main User object
        csv_path: path to additional CSV file
        dedupe_by_name: skip recipes with duplicate names (case-insensitive)

    Returns:
        (added_count, skipped_count)
    """
    # Import User class locally to avoid circular imports
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
