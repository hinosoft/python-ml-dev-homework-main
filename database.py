import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Đọc dữ liệu CSV
ingredients_df = pd.read_csv("sample-data/ingredients.csv")
recipes_df = pd.read_csv("sample-data/recipes.csv")

def add_recipe(recipe):
    new_recipe_id = recipes_df["recipe_id"].max() + 1
    for ing in recipe.ingredients:
        recipes_df.loc[len(recipes_df)] = [
            new_recipe_id, recipe.recipe_name, ing["ingredient_id"], ing["ingredient_name"],
            ing["quantity_in_grams"], recipe.recipe_type, recipe.cuisine
        ]
    recipes_df.to_csv("sample-data/recipes.csv", index=False)

def get_recipe_by_id(recipe_id: int):
    recipe_data = recipes_df[recipes_df["recipe_id"] == recipe_id]
    
    if recipe_data.empty:
        return None

    ingredients = recipe_data[["ingredient_id", "ingredient_name", "quantity_in_grams"]].to_dict(orient="records")
    return {
        "recipe_name": recipe_data["recipe_name"].iloc[0],
        "recipe_type": recipe_data["recipe_type"].iloc[0],
        "cuisine": recipe_data["cuisine"].iloc[0],
        "ingredients": ingredients
    }

def find_substitutes(ingredient_id: str):
    # Tìm giá trị dinh dưỡng của nguyên liệu cần thay thế
    target_nutrition = ingredients_df[ingredients_df["id"] == ingredient_id].iloc[:, 2:-2]
    
    if target_nutrition.empty:
        return None

    # Tính toán cosine similarity
    nutrition_values = ingredients_df.iloc[:, 2:-2].values
    similarity_scores = cosine_similarity([target_nutrition.values[0]], nutrition_values)[0]

    # Chọn 2-3 nguyên liệu có dinh dưỡng tương tự nhất
    sorted_indices = similarity_scores.argsort()[::-1][1:4]  # Bỏ chính nó, lấy 2-3 nguyên liệu thay thế
    substitutes = ingredients_df.iloc[sorted_indices][["id", "ingredient_name"]].to_dict(orient="records")

    return substitutes
