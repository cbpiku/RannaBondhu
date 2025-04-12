import pandas as pd
import random

# --- Load Recipes from Excel ---
def load_recipes(filename="food_recipe.xlsx"):
    df = pd.read_excel(filename)
    recipes = {}
    for _, row in df.iterrows():
        name = row["Recipe Name"].strip()
        ingredients = [i.strip().lower() for i in row["Ingredients"].split(",")]
        steps = [s.strip() for s in row["Steps"].split(",")]
        meal_type = row.get("Meal Time", "Any").strip()  # Get 'Meal Time', default to "Any" if missing
        recipes[name] = {"ingredients": ingredients, "steps": steps, "meal_type": meal_type}
    return recipes

# --- Step 1: Gather User Preferences ---
def get_user_preferences():
    print("👋 Let's set up your TasteAI profile.")
    diet = input("🟢 Veg / 🟠 Non-Veg: ").strip().lower()
    dislikes = input("❌ Ingredients you dislike (comma-separated): ").strip().lower().split(",")
    return {"diet": diet, "dislikes": [i.strip() for i in dislikes]}

# --- Step 2: Input Pantry Inventory ---
def get_pantry_items():
    pantry = input("🧺 Enter ingredients in your fridge/pantry (comma-separated): ").strip().lower().split(",")
    return [item.strip() for item in pantry]

# --- Step 3: Suggest Meals Based on Pantry ---
def suggest_meals(preferences, pantry, recipes):
    print("\n🔍 Finding recipes based on your pantry...")
    valid_recipes = []
    for recipe, details in recipes.items():
        is_veg = all(item not in ["fish", "meat", "chicken"] for item in details["ingredients"])
        
        # Check diet compatibility
        if preferences["diet"] == "veg" and not is_veg:
            continue
        if preferences["diet"] == "non-veg" and is_veg:
            continue
            
        if all(item in pantry for item in details["ingredients"]) and not any(d in details["ingredients"] for d in preferences["dislikes"]):
            valid_recipes.append(recipe)
            
    if not valid_recipes:
        print("🙁 Sorry, couldn't match any full recipes. Here’s a close match suggestion:")
        
        # Suggest a partial match based on diet
        eligible_recipes = [recipe for recipe, details in recipes.items() 
                            if (preferences["diet"] == "veg" and all(item not in ["fish", "meat", "chicken"] for item in details["ingredients"])) or
                               (preferences["diet"] == "non-veg" and any(item in ["fish", "meat", "chicken"] for item in details["ingredients"]))]
        
        if eligible_recipes:
            partial = random.choice(eligible_recipes)
            print(f"👉 {partial} (You might need to shop a few things!)")
            return [partial]
        else:
            print("👉 No recipes match your preferences and pantry.")
            return []
            
    print("✅ You can cook:")
    for r in valid_recipes:
        print(f"🍽️ {r}")
    return valid_recipes

# --- Step 4: Generate Smart Grocery List ---
def generate_grocery_list(selected_recipe, pantry, recipes):
    print("\n🛒 Generating smart grocery list...")
    needed = [i for i in recipes[selected_recipe]["ingredients"] if i not in pantry]
    if needed:
        print("🧾 You need to buy:")
        for item in needed:
            print(f"🛍️ {item}")
    else:
        print("🎉 You have everything you need!")

# --- Step 5: Step-by-Step Cooking Instructions ---
def cook_recipe(recipe_name, recipes):
    print(f"\n👨‍🍳 Cooking {recipe_name} - Step by Step:")
    for i, step in enumerate(recipes[recipe_name]["steps"], 1):
        input(f"\n➡️ Step {i}: {step}\n(Press Enter to continue)")

# --- Main Flow ---
def main():
    recipes = load_recipes()
    preferences = get_user_preferences()
    pantry = get_pantry_items()
    suggestions = suggest_meals(preferences, pantry, recipes)
    
    if suggestions:
        print("\n📋 Select a recipe to cook:")
        for idx, recipe in enumerate(suggestions, 1):
            print(f"{idx}. {recipe}")
        
        while True:
            try:
                choice = int(input("\n🔢 Enter the number of the recipe you want to cook: "))
                if 1 <= choice <= len(suggestions):
                    selected = suggestions[choice - 1]
                    break
                else:
                    print("❗ Invalid choice. Try again.")
            except ValueError:
                print("❗ Please enter a valid number.")

        generate_grocery_list(selected, pantry, recipes)
        cook_now = input(f"\n🍳 Want to start cooking {selected}? (yes/no): ").strip().lower()
        if cook_now == "yes":
            cook_recipe(selected, recipes)
        else:
            print("🕐 You can come back to this recipe later!")

if __name__ == "__main__":
    main()
