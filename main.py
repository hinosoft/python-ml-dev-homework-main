from fastapi import FastAPI
from database import get_recipe_by_id
from utils import calculate_total_cost, calculate_nutrition

app = FastAPI()

@app.get("/recipes/{recipe_id}/")
async def get_recipe(recipe_id: int):
    recipe = get_recipe_by_id(recipe_id)
    total_cost = calculate_total_cost(recipe)
    nutrition = calculate_nutrition(recipe)
    return {
        "recipe": recipe,
        "total_cost": total_cost,
        "nutrition": nutrition
    }
