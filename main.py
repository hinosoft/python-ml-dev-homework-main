from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import get_recipe_by_id, add_recipe, find_substitutes
from utils import calculate_total_cost, calculate_nutrition

app = FastAPI()

# Định nghĩa dữ liệu đầu vào cho API POST
class RecipeCreate(BaseModel):
    recipe_name: str
    recipe_type: str
    cuisine: str
    ingredients: list[dict]  # Danh sách nguyên liệu

@app.post("/recipes/")
async def create_recipe(recipe: RecipeCreate):
    add_recipe(recipe)  # Thêm recipe vào database
    return {"message": "Recipe added successfully", "recipe": recipe}

@app.get("/recipes/{recipe_id}/")
async def get_recipe(recipe_id: int):
    recipe = get_recipe_by_id(recipe_id)
    
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")

    total_cost = calculate_total_cost(recipe)
    nutrition = calculate_nutrition(recipe)

    return {
        "recipe": recipe,
        "total_cost": total_cost,
        "nutrition": nutrition
    }

@app.get("/ingredients/{ingredient_id}/substitutes/")
async def get_substitutes(ingredient_id: str):
    substitutes = find_substitutes(ingredient_id)

    if not substitutes:
        raise HTTPException(status_code=404, detail="No substitutes found")

    return {"ingredient_id": ingredient_id, "substitutes": substitutes}
