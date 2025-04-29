import pandas as pd

# Đọc dữ liệu từ file ingredients.csv
ingredients_df = pd.read_csv("sample-data/ingredients.csv")
# Hàm chuyển đổi ID
def convert_id_to_number(ingredient_id: str) -> int:
    return int(ingredient_id.split("_")[1])  # Lấy phần số sau "ing_" và chuyển thành int

# Áp dụng hàm cho cột "id"
ingredients_df["numeric_id"] = ingredients_df["id"].apply(convert_id_to_number)

# Kiểm tra kết quả
print(ingredients_df[["id", "numeric_id"]].head())

def calculate_total_cost(recipe):
    return sum(ingredients_df[ingredients_df["numeric_id"] == ing["ingredient_id"]]["cost_per_gram"].values[0] * ing["quantity_in_grams"] for ing in recipe["ingredients"])

def calculate_nutrition(recipe):
    nutrition_totals = {}
    for ing in recipe["ingredients"]:
        ingredient_data = ingredients_df[ingredients_df["numeric_id"] == ing["ingredient_id"]].to_dict(orient="records")[0]
        for key in ["energy", "carb", "protein", "fat"]:
            nutrition_totals[key] = nutrition_totals.get(key, 0) + (ingredient_data[key] * ing["quantity_in_grams"] / 100)
    return nutrition_totals
