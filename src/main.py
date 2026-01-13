 # RECIPE SELECTION SYSTEM  
#==================================================================
from abc import ABC, abstractmethod
import time


                        #  RECIPE CLASS 
class Recipe:
    """Stores information about a single recipe"""
    
    def __init__(self, name, category, price, cooking_time, ingredients, steps):
        self.name = name
        self.category = category  # soup, starter, main, dessert
        self.price = price  # estimated price in dollars
        self.cooking_time = cooking_time  # in minutes
        self.ingredients = ingredients  # list of ingredients
        self.steps = steps  # cooking instructions
    
    def display(self):
        """Print recipe details in a nice format"""
        print(f"\n{'='*50}")
        print(f"Recipe: {self.name}")
        print(f"{'='*50}")
        print(f"Category: {self.category}")
        print(f"Price: ${self.price:.2f}")
        print(f"Cooking Time: {self.cooking_time} minutes")
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
        result = recipes.copy()  # Don't modify original list
        
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
            print(f"{i}. {recipe.name} ({recipe.category}) - ${recipe.price:.2f}, {recipe.cooking_time} min")
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
                        print(f"  {i}. {recipe.name} - ${value:.2f}, {recipe.cooking_time} min")
                    else:
                        print(f"  {i}. {recipe.name} - {value} min, ${recipe.price:.2f}")
            
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
                else:
                    print(f"{i}. {recipe.name} - {value} min")
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
def performance_test(user, sort_key="cooking_time", runs=500):
    """Simple timing comparison: Bubble Sort (loop) vs Merge Sort (recursion)."""

    if len(user.recipes) < 2:
        print("⚠️ Not enough recipes to run performance test.")
        return

    # Bubble sort timing
    start = time.time()
    for _ in range(runs):
        _ = user.loop_sorter.sort(user.recipes.copy(), sort_key)
    bubble_time = time.time() - start

    # Merge sort timing
    start = time.time()
    for _ in range(runs):
        _ = user.recursion_sorter.sort(user.recipes.copy(), sort_key)
    merge_time = time.time() - start

    print("\n" + "=" * 50)
    print("PERFORMANCE TEST")
    print("=" * 50)
    print(f"Runs: {runs}, Sort key: {sort_key}")
    print(f"Loop-based Bubble Sort:     {bubble_time:.6f} seconds")
    print(f"Recursion-based Merge Sort: {merge_time:.6f} seconds")
    print("\nBig-O (theory):")
    print("- Bubble Sort: O(n^2)")
    print("- Merge Sort:  O(n log n)")
    print("=" * 50 + "\n")




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
    print("6. Search by Category")
    print("7. Sort Recipes")
    print("8. Export recipes to CSV")
    print("9. Performance test")
    print("10. Exit")

    print("="*50)


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
        choice = input("Enter your choice (1-10): ")
        
        if choice == "1":
            # View all recipes
            user.display_all_recipes()
        
        elif choice == "2":
            # View recipe details
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
            # Add new recipe
            add_new_recipe_interactive(user)
        
        elif choice == "4":
            # Edit recipe
            user.display_all_recipes()
            try:
                index = int(input("Enter recipe number to edit: ")) - 1
                user.edit_recipe(index)
            except ValueError:
                print("❌ Please enter a valid number!")
        
        elif choice == "5":
            # Delete recipe
            user.display_all_recipes()
            try:
                index = int(input("Enter recipe number to delete: ")) - 1
                user.delete_recipe(index)
            except ValueError:
                print("❌ Please enter a valid number!")
        
        elif choice == "6":
            # Search by category
            print("\nAvailable categories: soup, starter, main, dessert")
            category = input("Enter category: ")
            user.search_by_category(category)
        
        elif choice == "7":
            # Sort recipes
            print("\nSort by:")
            print("1. Price")
            print("2. Cooking Time")
            sort_choice = input("Enter choice (1-2): ")
            
            print("\nUse logical filter? (Cheap AND Quick recipes first)")
            print("Filter: price ≤ $10 AND cooking_time ≤ 30 minutes")
            print("1. Yes (with filter)")
            print("2. No (regular sort)")
            filter_choice = input("Enter choice (1-2): ")
            
            print("\nSorting method:")
            print("1. Loop-based (Bubble Sort)")
            print("2. Recursion-based (Merge Sort)")
            method_choice = input("Enter choice (1-2): ")
            
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
            else:
                print("❌ Invalid choice!")

        elif choice == "8":
            # Export recipes to CSV
            try:
                from io_csv import save_user_recipes_to_csv
                save_user_recipes_to_csv(user, "data/recipes_export.csv")
                print("✅ Exported to data/recipes_export.csv")
            except Exception as e:
                print("❌ Export failed:", e)

        elif choice == "9":
            performance_test(user, sort_key="cooking_time", runs=500)

        elif choice == "10":
            print("\n👋 Thank you for using the Recipe Selection System!")
            break
            
            # Exit program
            print("\n👋 Thank you for using the Recipe Selection System!")
            break

        
        else:
            print("\n❌ Invalid choice! Please enter 1-10.")
        
        input("\nPress Enter to continue...")

#=====================================================================================================
                    #  RUN PROGRAM  
if __name__ == "__main__":
    main()