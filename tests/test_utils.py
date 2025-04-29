from utils import calculate_total_cost, calculate_nutrition

def test_calculate_total_cost():
    recipe = {
        "ingredients": [
            {"ingredient_id": "3", "quantity_in_grams": 250},
            {"ingredient_id": "6", "quantity_in_grams": 100}
        ]
    }
    total_cost = calculate_total_cost(recipe)
    assert total_cost > 0

def test_calculate_nutrition():
    recipe = {
        "ingredients": [
            {"ingredient_id": "3", "quantity_in_grams": 250},
            {"ingredient_id": "6", "quantity_in_grams": 100}
        ]
    }
    nutrition = calculate_nutrition(recipe)
    assert nutrition["energy"] > 0
