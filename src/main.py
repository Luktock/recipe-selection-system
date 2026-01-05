import pandas as pd

def load_recipes():
    file_path = "data/recipes.csv"
    recipes = pd.read_csv(file_path)
    return recipes

def main():
    recipes = load_recipes()
    print("Recipe Selection System started")
    print(f"Number of recipes loaded: {len(recipes)}")
    print(recipes.head())

if __name__ == "__main__":
    main()

