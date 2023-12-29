def calculate_s_points(calories, saturated_fat, sugar, protein, fiber):
    # Constants for point calculations
    calories_per_point = 30
    saturated_fat_per_point = 3
    sugar_per_point = 8
    protein_per_point = 10
    fiber_per_point = 3

    # Calculate points based on the provided formula
    points = (
            calories / calories_per_point +
            saturated_fat / saturated_fat_per_point +
            sugar / sugar_per_point -
            protein / protein_per_point -
            fiber / fiber_per_point
    )

    return points


def convert_cm_to_inches(cm):
    # 1 cm = 0.393701 inches
    return cm * 0.393701

def convert_kg_to_pounds(kg):
    # 1 kg = 2.20462 pounds
    return kg * 2.20462

def calculate_daily_points_allowance(gender, age, height_cm, activity, weight_kg, nursing=False, supplementing=False):
    # Convert values to inches and pounds
    height = convert_cm_to_inches(height_cm)
    weight = convert_kg_to_pounds(weight_kg)

    # Calculate points based on gender
    gender_points = 8 if gender.lower() == "male" else 2
    if gender.lower() == "female":
        gender_points += 10 if nursing else 5 if supplementing else 0

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

    return total_points_allowance
