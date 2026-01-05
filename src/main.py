import pandas as pd

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
 



def save_recipes(recipes):
    file_path = "data/recipes_updated.csv"
    recipes.to_csv(file_path, index=False)
    print(f"Saved to {file_path}")

def main():
    recipes = load_recipes()
    print("Welcome to the Recipe Selection System!")
    print(f"Number of recipes loaded: {len(recipes)}")

    while True:
        print("\nMain Menu")
        print("1. View all recipes")
        print("2. Order a recipe")
        print("3. Search recipes")
        print("4. Sort recipes")
        print("5. Add recipe")
        print("6. Edit recipe")
        print("7. Delete recipe")
        print("8. Performance test")
        print("9. Export updated CSV files")
        print("0. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            print(recipes[["id", "name", "category", "price", "time_min"]])

        elif choice == "2":
            show_recipe_details(recipes)
        
        elif choice == "8":
            print("Performance test is not implemented yet.")

        elif choice == "9":
            save_recipes(recipes)

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("This feature is not implemented yet.")

if __name__ == "__main__":
    main()
