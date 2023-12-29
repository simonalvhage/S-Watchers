import json
import calculate

with open('ica.json', 'r', encoding='utf-8') as file:
    lines = file.readlines()

# List to store modified recipes
modified_recipes = []

# Iterate through each line (recipe) and calculate points
for line in lines:
    recipe = json.loads(line)
    nutrition_info = recipe.get('nutrition', {})
    calories = float(''.join(nutrition_info.get('energy', '0').split('kCal')[0].split(" ")[-2:]))  # Extracting calories from "energy" field
    saturated_fat = float(nutrition_info.get('fat', '0').split(' ')[0])  # Extracting saturated fat from "fat" field
    sugar = float(nutrition_info.get('carbohydrates', '0').split(' ')[0])  # Extracting sugar from "carbohydrates" field
    protein = float(nutrition_info.get('protein', '0').split(' ')[0])  # Extracting protein from "protein" field
    fiber = 0  # Assuming there's no fiber information provided in your example

    # Calculate WW points using the function
    ww_points = calculate.calculate_s_points(calories, saturated_fat, sugar, protein, fiber)

    # Add the calculated points to the recipe
    recipe['S-Points'] = round(ww_points, 2)

    # Append the modified recipe to the list
    modified_recipes.append(recipe)

# Save the modified recipes to a new JSON file
with open('ica_modified.json', 'w', encoding='utf-8') as output_file:
    for modified_recipe in modified_recipes:
        # Write each modified recipe to the file
        output_file.write(json.dumps(modified_recipe, ensure_ascii=False) + '\n')