 # RECIPE SELECTION SYSTEM  
#==================================================================
from abc import ABC, abstractmethod
import time

                        #  RECIPE CLASS 
class Recipe:
    """Stores information about a single recipe"""
    
    def __init__(self, name, category, price, cooking_time, ingredients, steps, rating=0.0):
        self.name = name
        self.category = category  # soup, starter, main, dessert
        self.price = price  # estimated price in dollars
        self.cooking_time = cooking_time  # in minutes
        self.ingredients = ingredients  # list of ingredients
        self.steps = steps  # cooking instructions
        self.rating = rating

    
    def display(self):
        """Print recipe details in a nice format"""
        print(f"\n{'='*50}")
        print(f"Recipe: {self.name}")
        print(f"{'='*50}")
        print(f"Category: {self.category}")
        print(f"Price: ${self.price:.2f}")
        print(f"Cooking Time: {self.cooking_time} minutes")
        print(f"Rating: {self.rating:.1f}/5")
        print(f"\nIngredients:")
        for ingredient in self.ingredients:
            print(f"  - {ingredient}")
        print(f"\nSteps:")
        for i, step in enumerate(self.steps, 1):
            print(f"  {i}. {step}")
        print(f"{'='*50}\n")

#=====================================================================================================
                        # ABSTRACT SORTING CLASS 
class SortingAlgorithm(ABC):
    """Abstract base class for sorting algorithms"""
    
    @abstractmethod
    def sort(self, recipes, key):
        """Sort recipes based on a key (must be implemented by subclasses)"""
        pass


                        #   LOOP-BASED SORTING  
class LoopSorting(SortingAlgorithm):
    """Sorts recipes using loop-based bubble sort"""
    
    def sort(self, recipes, key):
        """Bubble sort using loops"""
        n = len(recipes)
        result = recipes.copy()  
        
        # Bubble sort algorithm using loops
        for i in range(n):
            for j in range(0, n - i - 1):
                # Compare adjacent elements
                if getattr(result[j], key) > getattr(result[j + 1], key):
                    # Swap if in wrong order
                    result[j], result[j + 1] = result[j + 1], result[j]
        
        return result

#=====================================================================================================
                    #   RECURSION-BASED SORTING  
class RecursionSorting(SortingAlgorithm):
    """Sorts recipes using recursion-based merge sort"""
    
    def sort(self, recipes, key):
        """Merge sort using recursion"""
        if len(recipes) <= 1:
            return recipes
        
        # Divide: split list in half
        mid = len(recipes) // 2
        left = self.sort(recipes[:mid], key)
        right = self.sort(recipes[mid:], key)
        
        # Conquer: merge sorted halves
        return self._merge(left, right, key)
    
    def _merge(self, left, right, key):
        """Helper method to merge two sorted lists"""
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            if getattr(left[i], key) <= getattr(right[j], key):
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        result.extend(left[i:])
        result.extend(right[j:])
        return result

#=====================================================================================================
                #   USER CLASS  
class User:
    """Manages the collection of recipes"""
    
    def __init__(self):
        self.recipes = []  # list to store all recipes
        self.loop_sorter = LoopSorting()  # Loop-based sorting
        self.recursion_sorter = RecursionSorting()  # Recursion-based sorting
    
    def add_recipe(self, recipe):
        """Add a new recipe to the collection"""
        self.recipes.append(recipe)
        print(f"✓ Recipe '{recipe.name}' added successfully!")
    
    def delete_recipe(self, index):
        """Delete a recipe by index"""
        if 0 <= index < len(self.recipes):
            removed = self.recipes.pop(index)
            print(f"✓ Recipe '{removed.name}' deleted successfully!")
            return True
        else:
            print("❌ Invalid recipe number!")
            return False
    
    def edit_recipe(self, index):
        """Edit an existing recipe"""
        if 0 <= index < len(self.recipes):
            recipe = self.recipes[index]
            print(f"\nEditing: {recipe.name}")
            print("(Press Enter to keep current value)")
            
            # Edit name
            new_name = input(f"Name [{recipe.name}]: ")
            if new_name:
                recipe.name = new_name
            
            # Edit category
            new_category = input(f"Category [{recipe.category}]: ")
            if new_category:
                recipe.category = new_category
            
            # Edit price
            new_price = input(f"Price [{recipe.price}]: ")
            if new_price:
                try:
                    recipe.price = float(new_price)
                except ValueError:
                    print("Invalid price, keeping original")
            
            # Edit cooking time
            new_time = input(f"Cooking Time [{recipe.cooking_time}]: ")
            if new_time:
                try:
                    recipe.cooking_time = int(new_time)
                except ValueError:
                    print("Invalid time, keeping original")
            
            # Edit ingredients
            edit_ing = input("\nEdit ingredients? (y/n): ")
            if edit_ing.lower() == 'y':
                print("Enter new ingredients (one per line, type 'done' when finished):")
                new_ingredients = []
                while True:
                    ingredient = input("- ")
                    if ingredient.lower() == 'done':
                        break
                    if ingredient:
                        new_ingredients.append(ingredient)
                if new_ingredients:
                    recipe.ingredients = new_ingredients
            
            # Edit steps
            edit_steps = input("Edit cooking steps? (y/n): ")
            if edit_steps.lower() == 'y':
                print("Enter new steps (one per line, type 'done' when finished):")
                new_steps = []
                while True:
                    step = input(f"{len(new_steps)+1}. ")
                    if step.lower() == 'done':
                        break
                    if step:
                        new_steps.append(step)
                if new_steps:
                    recipe.steps = new_steps
            
            print("✓ Recipe updated successfully!")
            return True
        else:
            print("❌ Invalid recipe number!")
            return False
    
    def display_all_recipes(self):
        """Show all recipes in the system"""
        if not self.recipes:
            print("\n⚠️  No recipes available yet!")
            return
        
        print(f"\n{'='*50}")
        print(f"ALL RECIPES ({len(self.recipes)} total)")
        print(f"{'='*50}")
        for i, recipe in enumerate(self.recipes, 1):
            print(f"{i}. {recipe.name} ({recipe.category}) - ${recipe.price:.2f}, {recipe.cooking_time} min, ⭐ {recipe.rating:.1f}/5")
        print(f"{'='*50}\n")
    
    def search_by_category(self, category):
        """Find all recipes in a specific category"""
        results = [r for r in self.recipes if r.category.lower() == category.lower()]
        
        if not results:
            print(f"\n⚠️  No recipes found in category '{category}'")
            return
        
        print(f"\n{'='*50}")
        print(f"RECIPES IN CATEGORY: {category.upper()}")
        print(f"{'='*50}")
        for recipe in results:
            print(f"- {recipe.name} (${recipe.price:.2f}, {recipe.cooking_time} min)")
        print(f"{'='*50}\n")

# (4) SEARCHING FUNCTIONS (Ramya)
    def search_by_name(self, name_query):
        """Search recipes by (partial) name match"""
        if not self.recipes:
            print("\n⚠️  No recipes available to search!")
            return []

        q = name_query.strip().lower()
        results = [r for r in self.recipes if q in r.name.lower()]

        if not results:
            print(f"\n⚠️  No recipes found with name containing '{name_query}'.")
            return []

        print(f"\n{'='*50}")
        print(f"SEARCH RESULTS (NAME CONTAINS: {name_query})")
        print(f"{'='*50}")
        for i, recipe in enumerate(results, 1):
            print(f"{i}. {recipe.name} ({recipe.category}) - ${recipe.price:.2f}, {recipe.cooking_time} min")
        print(f"{'='*50}\n")
        return results

    def search_by_ingredient(self, ingredient_query):
        """Search recipes containing a specific ingredient (case-insensitive, partial match)"""
        if not self.recipes:
            print("\n⚠️  No recipes available to search!")
            return []

        q = ingredient_query.strip().lower()

        def has_ingredient(recipe):
            return any(q in ing.lower() for ing in recipe.ingredients)

        results = [r for r in self.recipes if has_ingredient(r)]

        if not results:
            print(f"\n⚠️  No recipes found containing ingredient '{ingredient_query}'.")
            return []

        print(f"\n{'='*50}")
        print(f"RECIPES CONTAINING: {ingredient_query}")
        print(f"{'='*50}")
        for i, recipe in enumerate(results, 1):
            print(f"{i}. {recipe.name} ({recipe.category}) - ${recipe.price:.2f}, {recipe.cooking_time} min")
        print(f"{'='*50}\n")
        return results

    def search_include_exclude_ingredients(self, include_ingredient, exclude_ingredient):
        """Search recipes that include X but NOT Y (case-insensitive, partial match)."""
        if not self.recipes:
            print("\n⚠️  No recipes available to search!")
            return []

        inc = include_ingredient.strip().lower()
        exc = exclude_ingredient.strip().lower()

        def includes(recipe):
            return any(inc in ing.lower() for ing in recipe.ingredients)

        def excludes(recipe):
            return all(exc not in ing.lower() for ing in recipe.ingredients)

        results = [r for r in self.recipes if includes(r) and excludes(r)]

        if not results:
            print(f"\n⚠️  No recipes found that include '{include_ingredient}' but not '{exclude_ingredient}'.")
            return []

        print(f"\n{'='*50}")
        print(f"RECIPES: include '{include_ingredient}' AND NOT '{exclude_ingredient}'")
        print(f"{'='*50}")
        for i, recipe in enumerate(results, 1):
            print(f"{i}. {recipe.name} - Ingredients: {', '.join(recipe.ingredients)}")
        print(f"{'='*50}\n")
        return results
    
    def sort_recipes(self, sort_by, use_recursion=False, use_logical_filter=False):
        """Sort recipes using either loop or recursion algorithm"""
        if not self.recipes:
            print("\n⚠️  No recipes to sort!")
            return
        
        recipes_to_sort = self.recipes
        
        # Apply logical filter if requested (secondary sorting key)
        if use_logical_filter:
            # Logical expression: "cheap AND quick" (price <= 10 AND cooking_time <= 30)
            filtered = [r for r in self.recipes if r.price <= 10 and r.cooking_time <= 30]
            not_filtered = [r for r in self.recipes if not (r.price <= 10 and r.cooking_time <= 30)]
            
            # Choose sorting algorithm
            if use_recursion:
                sorted_filtered = self.recursion_sorter.sort(filtered, sort_by)
                sorted_not_filtered = self.recursion_sorter.sort(not_filtered, sort_by)
                method = "Recursion (Merge Sort)"
            else:
                sorted_filtered = self.loop_sorter.sort(filtered, sort_by)
                sorted_not_filtered = self.loop_sorter.sort(not_filtered, sort_by)
                method = "Loop (Bubble Sort)"
            
            # Combine: logical TRUE recipes first, then FALSE
            sorted_recipes = sorted_filtered + sorted_not_filtered
            
            print(f"\n{'='*50}")
            print(f"SORTED BY {sort_by.upper()} WITH LOGICAL FILTER")
            print(f"Using {method}")
            print(f"Filter: Cheap (≤$10) AND Quick (≤30 min) recipes first")
            print(f"{'='*50}")
            
            if sorted_filtered:
                print("\n✓ MATCHES FILTER (Cheap AND Quick):")
                for i, recipe in enumerate(sorted_filtered, 1):
                    value = getattr(recipe, sort_by)

                    if sort_by == "price":
                        print(f"{i}. {recipe.name} - ${value:.2f}")
                    elif sort_by == "cooking_time":
                        print(f"{i}. {recipe.name} - {value} min")
                    elif sort_by == "rating":
                        print(f"{i}. {recipe.name} - ⭐ {value:.1f}/5")
                    else:
                        print(f"{i}. {recipe.name} - {value}")


            
            if sorted_not_filtered:
                print("\n○ Does not match filter:")
                for i, recipe in enumerate(sorted_not_filtered, len(sorted_filtered) + 1):
                    value = getattr(recipe, sort_by)
                    if sort_by == "price":
                        print(f"  {i}. {recipe.name} - ${value:.2f}, {recipe.cooking_time} min")
                    else:
                        print(f"  {i}. {recipe.name} - {value} min, ${recipe.price:.2f}")
            
            print(f"{'='*50}\n")
        
        else:
            # Regular sorting without logical filter
            if use_recursion:
                sorted_recipes = self.recursion_sorter.sort(self.recipes, sort_by)
                method = "Recursion (Merge Sort)"
            else:
                sorted_recipes = self.loop_sorter.sort(self.recipes, sort_by)
                method = "Loop (Bubble Sort)"
            
            print(f"\n{'='*50}")
            print(f"SORTED BY {sort_by.upper()} - Using {method}")
            print(f"{'='*50}")
            for i, recipe in enumerate(sorted_recipes, 1):
                value = getattr(recipe, sort_by)
                if sort_by == "price":
                    print(f"{i}. {recipe.name} - ${value:.2f}")
                elif sort_by == "cooking_time":
                    print(f"{i}. {recipe.name} - {value} min")
                elif sort_by == "rating":
                    print(f"{i}. {recipe.name} - ⭐ {value:.1f}/5")
                else:
                    print(f"{i}. {recipe.name} - {value}")
            print(f"{'='*50}\n")
        
        # Update internal list with sorted result
        self.recipes = sorted_recipes

#=====================================================================================================
            #   ADD NEW RECIPE 
def add_new_recipe_interactive(user):
    """Add a new recipe through user input"""
    print("\n" + "="*50)
    print("ADD NEW RECIPE")
    print("="*50)
    
    name = input("Recipe Name: ")
    category = input("Category (soup/starter/main/dessert): ")
    
    try:
        price = float(input("Estimated Price ($): "))
        cooking_time = int(input("Cooking Time (minutes): "))
    except ValueError:
        print("❌ Invalid price or time! Recipe not added.")
        return
    
    print("\nEnter ingredients (one per line, type 'done' when finished):")
    ingredients = []
    while True:
        ingredient = input("- ")
        if ingredient.lower() == 'done':
            break
        if ingredient:
            ingredients.append(ingredient)
    
    print("\nEnter cooking steps (one per line, type 'done' when finished):")
    steps = []
    while True:
        step = input(f"{len(steps)+1}. ")
        if step.lower() == 'done':
            break
        if step:
            steps.append(step)
    
    new_recipe = Recipe(name, category, price, cooking_time, ingredients, steps)
    user.add_recipe(new_recipe)
#================================================================================================
                                   # Performance function
def performance_test(user, sort_key="cooking_time"):
    """Performance analysis: Bubble (loop) vs Merge (recursion) with 2 measurements."""

    if len(user.recipes) < 2:
        print("⚠️ Not enough recipes to run performance test.")
        return

    def time_sort(sort_func, data, runs):
        start = time.time()
        for _ in range(runs):
            _ = sort_func(data.copy(), sort_key)
        return time.time() - start

    base = user.recipes.copy()

    # Measurement 1: small dataset (a bit larger than base for meaningful results)
    data_small = base * 5

    # Measurement 2: large dataset (simulate complexity)
    data_large = base * 50

    # Demo-safe runs
    runs_small = 200
    runs_large = 20

    bubble_small = time_sort(user.loop_sorter.sort, data_small, runs_small)
    merge_small  = time_sort(user.recursion_sorter.sort, data_small, runs_small)

    bubble_large = time_sort(user.loop_sorter.sort, data_large, runs_large)
    merge_large  = time_sort(user.recursion_sorter.sort, data_large, runs_large)

    print("\n" + "=" * 60)
    print("PERFORMANCE ANALYSIS")
    print("=" * 60)
    print(f"Runs: small={runs_small}, large={runs_large} | Sort key: {sort_key}")

    print("\nMeasurement 1: small dataset")
    print(f"n = {len(data_small)}")
    print(f"  Bubble Sort (loop):      {bubble_small:.6f}s")
    print(f"  Merge Sort  (recursion): {merge_small:.6f}s")

    print("\nMeasurement 2: large dataset")
    print(f"n = {len(data_large)}")
    print(f"  Bubble Sort (loop):      {bubble_large:.6f}s")
    print(f"  Merge Sort  (recursion): {merge_large:.6f}s")

    print("\nBig-O (theory):")
    print("- Bubble Sort: O(n^2)")
    print("- Merge Sort:  O(n log n)")

    print("\nInterpretation:")
    print("- For smaller datasets, overhead can make merge sort slower than bubble sort.")
    print("- As dataset size grows, merge sort scales better (n log n) than bubble sort (n^2).")

    print("=" * 60 + "\n")








#=====================================================================================================
            #   MAIN MENU 
def display_menu():
    """Show the main menu options"""
    print("\n" + "="*50)
    print("     INTELLIGENT RECIPE SELECTION SYSTEM")
    print("="*50)
    print("1. View All Recipes")
    print("2. View Recipe Details")
    print("3. Add New Recipe")
    print("4. Edit Recipe")
    print("5. Delete Recipe")
    print("6. Search recipes (name / category / ingredient)")
    print("7. Sort Recipes")
    print("8. Export recipes to CSV")
    print("9. Import recipes from CSV")
    print("10. Rate a recipe")
    print("11. Performance test")
    print("12. Exit")



    print("="*50)


def rate_recipe(user):
    """Let user rate a recipe (0 to 5)."""
    if not user.recipes:
        print("⚠️ No recipes available to rate.")
        return

    user.display_all_recipes()

    try:
        index = int(input("Enter recipe number to rate: ")) - 1
        if not (0 <= index < len(user.recipes)):
            print("❌ Invalid recipe number!")
            return

        rating = float(input("Enter rating (0-5): "))
        if rating < 0 or rating > 5:
            print("❌ Rating must be between 0 and 5.")
            return

        user.recipes[index].rating = rating
        print(f"✅ Rated '{user.recipes[index].name}' with {rating:.1f}/5")

    except ValueError:
        print("❌ Please enter a valid number.")


def main():
    """Main program execution"""

    # Create user and load recipes from CSV
    user = User()

    try:
        from io_csv import load_recipes_into_user
        load_recipes_into_user(user, "data/recipes.csv")
        print("\n🍳 Welcome to the Recipe Selection System!")
        print(f"{len(user.recipes)} recipes loaded from CSV.\n")
    except FileNotFoundError as e:
        print("\n⚠️ CSV file not found. Starting with empty recipe list.")
        print(e)
    except Exception as e:
        print("\n⚠️ Error while loading recipes from CSV.")
        print(e)



    
        # Main program loop
    while True:
        display_menu()
        choice = input("Enter your choice (1-12): ").strip()


        if choice == "1":
            user.display_all_recipes()

        elif choice == "2":
            user.display_all_recipes()
            try:
                index = int(input("Enter recipe number to view details: ")) - 1
                if 0 <= index < len(user.recipes):
                    user.recipes[index].display()
                else:
                    print("❌ Invalid recipe number!")
            except ValueError:
                print("❌ Please enter a valid number!")

        elif choice == "3":
            add_new_recipe_interactive(user)

        elif choice == "4":
            user.display_all_recipes()
            try:
                index = int(input("Enter recipe number to edit: ")) - 1
                user.edit_recipe(index)
            except ValueError:
                print("❌ Please enter a valid number!")

        elif choice == "5":
            user.display_all_recipes()
            try:
                index = int(input("Enter recipe number to delete: ")) - 1
                user.delete_recipe(index)
            except ValueError:
                print("❌ Please enter a valid number!")

        elif choice == "6":
            print("\nSearch options:")
            print("1. By name")
            print("2. By category")
            print("3. By ingredient")
            print("4. Ingredient include X but NOT Y")
            search_choice = input("Choose (1-4): ").strip()

            if search_choice == "1":
                term = input("Enter name keyword: ")
                results = user.search_by_name(term)

            elif search_choice == "2":
                print("\nAvailable categories: soup, starter, main, dessert")
                category = input("Enter category: ")
                user.search_by_category(category)
                results = None  # already printed inside method

            elif search_choice == "3":
                ing = input("Enter ingredient keyword: ")
                results = user.search_by_ingredient(ing)


            elif search_choice == "4":
                ing = input("Include ingredient keyword: ")
                ex = input("Exclude ingredient keyword: ")
                results = user.search_include_exclude_ingredients(ing, ex)


            else:
                print("❌ Invalid search choice.")
                results = None


        elif choice == "7":
            print("\nSort by:")
            print("1. Price")
            print("2. Cooking Time")
            print("3. Rating")
            sort_choice = input("Enter choice (1-3): ").strip()
            print("\nUse logical filter? (Cheap AND Quick recipes first)")
            print("Filter: price ≤ $10 AND cooking_time ≤ 30 minutes")
            print("1. Yes (with filter)")
            print("2. No (regular sort)")
            filter_choice = input("Enter choice (1-2): ").strip()

            print("\nSorting method:")
            print("1. Loop-based (Bubble Sort)")
            print("2. Recursion-based (Merge Sort)")
            method_choice = input("Enter choice (1-2): ").strip()

            if sort_choice == "1":
                user.sort_recipes(
                        "price",
                        use_recursion=(method_choice == "2"),
                     use_logical_filter=(filter_choice == "1")
                    )

            elif sort_choice == "2":
                user.sort_recipes(
                    "cooking_time",
                    use_recursion=(method_choice == "2"),
                    use_logical_filter=(filter_choice == "1")
                )

            elif sort_choice == "3":
                user.sort_recipes(
                    "rating",
                    use_recursion=(method_choice == "2"),
                    use_logical_filter=(filter_choice == "1")
                )

            else:
                print("❌ Invalid choice!")


        elif choice == "8":
            try:
                from io_csv import save_user_recipes_to_csv
                save_user_recipes_to_csv(user, "data/recipes_export.csv")
                print("✅ Exported to data/recipes_export.csv")
            except Exception as e:
                print("❌ Export failed:", e)

        elif choice == "9":
            path = input("Enter path to CSV file to import: ").strip()
            if not path:
                print("❌ Please enter a CSV file path (e.g. data/more_recipes.csv).")
                continue

            try:
                from io_csv import import_recipes_into_user
                added, skipped = import_recipes_into_user(user, path)
                print(f"✅ Import successful. Added: {added}, Skipped duplicates: {skipped}")
            except FileNotFoundError:
                print("❌ File not found.")
            except Exception as e:
                print("❌ Import failed:", e)

        elif choice == "10":
            rate_recipe(user)

        elif choice == "11":
            performance_test(user)


        elif choice == "12":
            print("\n👋 Thank you for using the Recipe Selection System!")
            break

        else:
            print("\n❌ Invalid choice! Please enter 1–12.")

        input("\nPress Enter to continue...")



#=====================================================================================================
                    #  RUN PROGRAM  
if __name__ == "__main__":
    main()
