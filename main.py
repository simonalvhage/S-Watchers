import json
import tkinter as tk
from tkinter import ttk
import webbrowser

class RecipeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Recipe App")

        # Left Frame for Daily Points Calculator
        self.left_frame = ttk.Frame(self.root)
        self.left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.setup_calculator_gui()

        # Right Frame for Recipe List
        self.right_frame = ttk.Frame(self.root)
        self.right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.setup_recipe_list_gui()

        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)

    def convert_cm_to_inches(self, cm):
        return cm * 0.393701

    def convert_kg_to_pounds(self, kg):
        return kg * 2.20462

    def calculate_daily_points_allowance(self):
        gender = self.gender_var.get()
        age = int(self.age_entry.get())
        height_cm = float(self.height_entry.get())
        activity = self.activity_var.get()
        weight_kg = float(self.weight_entry.get())

        # Convert values to inches and pounds
        height = self.convert_cm_to_inches(height_cm)
        weight = self.convert_kg_to_pounds(weight_kg)

        # Calculate points based on gender
        gender_points = 8 if gender.lower() == "male" else 2
        if gender.lower() == "female":
            gender_points += 10 if self.nursing_var.get() else 5 if self.supplementing_var.get() else 0

        # Calculate points based on age
        if 17 <= age <= 26:
            age_points = 4
        elif 27 <= age <= 37:
            age_points = 3
        elif 38 <= age <= 47:
            age_points = 2
        elif 48 <= age <= 58:
            age_points = 1
        else:
            age_points = 0

        # Calculate points based on height
        if height < 61:
            height_points = 0
        elif 61 <= height <= 70:
            height_points = 1
        else:
            height_points = 2

        # Calculate points based on activity
        if activity.lower() == "sitting":
            activity_points = 0
        elif activity.lower() == "light training":
            activity_points = 2
        elif activity.lower() == "training":
            activity_points = 4
        elif activity.lower() == "heavy training":
            activity_points = 6

        # Calculate points based on weight
        weight_points = int(str(int(weight))[:2])  # Add the first 2 digits of weight

        # Calculate total points allowance
        total_points_allowance = gender_points + age_points + height_points + activity_points + weight_points

        # Display the result
        self.result_label.config(text=f"Your daily points allowance: {total_points_allowance}")

    def setup_calculator_gui(self):
        # Age Entry
        age_label = ttk.Label(self.left_frame, text="Age:")
        age_label.grid(row=1, column=0, pady=5, sticky="w")

        self.age_entry = ttk.Entry(self.left_frame)
        self.age_entry.grid(row=1, column=1, pady=5, sticky="w")

        # Height Entry
        height_label = ttk.Label(self.left_frame, text="Height (cm):")
        height_label.grid(row=2, column=0, pady=5, sticky="w")

        self.height_entry = ttk.Entry(self.left_frame)
        self.height_entry.grid(row=2, column=1, pady=5, sticky="w")

        # Weight Entry
        weight_label = ttk.Label(self.left_frame, text="Weight (kg):")
        weight_label.grid(row=3, column=0, pady=5, sticky="w")

        self.weight_entry = ttk.Entry(self.left_frame)
        self.weight_entry.grid(row=3, column=1, pady=5, sticky="w")

        # Gender Dropdown
        gender_label = ttk.Label(self.left_frame, text="Gender:")
        gender_label.grid(row=4, column=0, pady=5, sticky="w")

        self.gender_var = tk.StringVar(self.left_frame)
        gender_options = ["Male", "Female"]
        self.gender_dropdown = ttk.Combobox(self.left_frame, textvariable=self.gender_var, values=gender_options)
        self.gender_dropdown.grid(row=4, column=1, pady=5, sticky="w")

        # Activity Dropdown
        activity_label = ttk.Label(self.left_frame, text="Activity:")
        activity_label.grid(row=5, column=0, pady=5, sticky="w")

        self.activity_var = tk.StringVar(self.left_frame)
        activity_options = ["Sitting", "Light Training", "Training", "Heavy Training"]
        self.activity_dropdown = ttk.Combobox(self.left_frame, textvariable=self.activity_var, values=activity_options)
        self.activity_dropdown.grid(row=5, column=1, pady=5, sticky="w")

        # Nursing Checkbox
        self.nursing_var = tk.BooleanVar(self.left_frame)
        nursing_checkbox = ttk.Checkbutton(self.left_frame, text="Nursing", variable=self.nursing_var)
        nursing_checkbox.grid(row=6, column=0, columnspan=2, pady=5, sticky="w")

        # Supplementing Checkbox
        self.supplementing_var = tk.BooleanVar(self.left_frame)
        supplementing_checkbox = ttk.Checkbutton(self.left_frame, text="Supplementing", variable=self.supplementing_var)
        supplementing_checkbox.grid(row=7, column=0, columnspan=2, pady=5, sticky="w")

        # Calculate Button
        calculate_button = ttk.Button(self.left_frame, text="Calculate Points", command=self.calculate_daily_points_allowance)
        calculate_button.grid(row=8, column=0, columnspan=2, pady=10)

        # Result Label
        self.result_label = ttk.Label(self.left_frame, text="")
        self.result_label.grid(row=9, column=0, columnspan=2, pady=10)

    def populate_recipe_list(self):
        # Read and parse the recipe data from the JSON file
        with open("ica_modified.json", "r", encoding="utf-8") as file:
            lines = file.readlines()

            recipes = [json.loads(line) for line in lines if "nutrition" in line and "S-Points" in line]

        for recipe in recipes:
            # Skip recipes with S-Points less than or equal to 0
            if recipe.get("S-Points", 0) > 0:
                title = recipe.get("title", "")
                cooking_time = recipe.get("cookingTime", "")
                difficulty = recipe.get("difficulty", "")
                num_ingredients = recipe.get("numberOfIngredients", "")
                s_points = recipe.get("S-Points", "")
                url = recipe.get("absoluteUrl", "")

                self.recipe_tree.insert("", "end", values=(title, cooking_time, difficulty, num_ingredients, s_points, url))

    def open_recipe_url(self, event):
        selected_item = self.recipe_tree.selection()
        if selected_item:
            url = self.recipe_tree.item(selected_item, "values")[-1]
            webbrowser.open(url)

    def setup_recipe_list_gui(self):
        self.recipe_tree = ttk.Treeview(self.right_frame, columns=("Title", "Cooking Time", "Difficulty", "Ingredients", "S-Points"))
        self.recipe_tree.heading("#0", text="", anchor="w")
        self.recipe_tree.heading("Title", text="Recipe Name", anchor="w")
        self.recipe_tree.heading("Cooking Time", text="Cooking Time", anchor="w")
        self.recipe_tree.heading("Difficulty", text="Difficulty", anchor="w")
        self.recipe_tree.heading("Ingredients", text="Num of Ingredients", anchor="w")
        self.recipe_tree.heading("S-Points", text="S-Points", anchor="w")

        self.recipe_tree.column("#0", width=1, stretch=tk.NO)
        self.recipe_tree.column("Title", anchor="w", width=150)
        self.recipe_tree.column("Cooking Time", anchor="w", width=100)
        self.recipe_tree.column("Difficulty", anchor="w", width=100)
        self.recipe_tree.column("Ingredients", anchor="w", width=120)
        self.recipe_tree.column("S-Points", anchor="w", width=80)

        self.recipe_tree.bind("<Double-1>", self.open_recipe_url)

        self.recipe_tree.grid(row=0, column=0, sticky="nsew")
        self.right_frame.rowconfigure(0, weight=1)
        self.right_frame.columnconfigure(0, weight=1)

        # Populate Recipe List
        self.populate_recipe_list()

if __name__ == "__main__":
    root = tk.Tk()
    app = RecipeApp(root)
    root.mainloop()
