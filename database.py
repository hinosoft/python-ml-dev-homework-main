import pandas as pd

# Đọc dữ liệu từ CSV
ingredients_df = pd.read_csv("sample-data/ingredients.csv")
recipes_df = pd.read_csv("sample-data/recipes.csv")

def get_recipe_by_id(recipe_id: int):
    recipe_data = recipes_df[recipes_df["recipe_id"] == recipe_id]

    # Kiểm tra nếu không tìm thấy recipe
    if recipe_data.empty:
        return None

    ingredients = recipe_data[["ingredient_id", "ingredient_name", "quantity_in_grams"]].to_dict(orient="records")
    return {
        "recipe_name": recipe_data["recipe_name"].iloc[0],
        "recipe_type": recipe_data["recipe_type"].iloc[0],
        "cuisine": recipe_data["cuisine"].iloc[0],
        "ingredients": ingredients
    }
