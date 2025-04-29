def calculate_total_cost(recipe):
    return sum(ingredients_df[ingredients_df["id"] == ing["ingredient_id"]]["cost_per_gram"].values[0] * ing["quantity_in_grams"] for ing in recipe["ingredients"])

def calculate_nutrition(recipe):
    nutrition_totals = {}
    for ing in recipe["ingredients"]:
        ingredient_data = ingredients_df[ingredients_df["id"] == ing["ingredient_id"]].to_dict(orient="records")[0]
        for key in ["energy", "carb", "protein", "fat"]:
            nutrition_totals[key] = nutrition_totals.get(key, 0) + (ingredient_data[key] * ing["quantity_in_grams"] / 100)
    return nutrition_totals
