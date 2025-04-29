from database import get_recipe_by_id

def test_get_recipe_by_id():
    recipe = get_recipe_by_id(1)
    assert recipe["recipe_name"] == "Hearty Vegetable Soup"
    assert len(recipe["ingredients"]) > 0
