import pandas as pd

def load_recipes():
    file_path = "data/recipes.csv"
    recipes = pd.read_csv(file_path)
    return recipes

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
        print("9. Export updated CSV files")
        print("0. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            print(recipes[["id", "name", "category", "price", "time_min"]])

        elif choice == "9":
            save_recipes(recipes)

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("This feature is not implemented yet.")

if __name__ == "__main__":
    main()
