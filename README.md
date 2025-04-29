# Python ML Dev Homework

We've created this basic test to allow you to demonstrate your skills outside the pressure of an interview.

We expect this should take a senior developer 2 - 3 hours to complete. And another 1 - 2 for the optional add-ons. 

We dont want you spending more than 4 hours on this. If you are unable to complete within this time, please submit what you have completed with details of how you would have finished or optimised it if you had more time.

---
## OVERVIEW
This FastAPI-based application provides a backend service for creating, calculating nutrition and cost of recipes, and suggesting ingredient substitutes based on nutritional analysis.
## RUN
### Run with Python
```
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
### Run with Docker
```
docker build -t fastapi-app .
docker run -d -p 8000:8000 fastapi-app
```
### Run with Docker Compose
```
docker-compose up --build
```
### API Endpoints:

#### `POST /recipes/`
– Create a new recipe

#### `GET /recipes/{id}/` 
– Retrieve recipe details, cost, and nutrition

#### `GET /v1/ingredients/{id}/substitutes/` 
– Suggest substitutes based on nutrition

### test
```
pytest
```
## Assignment

We would like you to design a small backend service to: 

1. Calculate total cost and nutritional values for recipes
2. Provide a simple API using **FastAPI**
3. Find substitute ingredients based on similarity

---
## Task 2: Suggest Ingredient Substitutes

### Add a basic substitute suggestion endpoint:
- **GET /ingredients/{id}/substitutes/**
  - Return 2-3 possible substitutes for an ingredient based on a similar nutrition profile (e.g., similar name, brand, calories or macros).
  - You can use any ML techniques to get the best matches. **Use of any LLM API is strictly prohibited**
  - (Optional) Create a test with one of the recipes utilizing this API
## What's Provided?

### Problem Approach
To identify the most suitable substitute ingredients from a large dataset, we employed the Approximate Nearest Neighbors (ANN) technique using the Faiss library by Facebook. This method is designed to efficiently handle high-dimensional data and rapidly find the nearest neighbors in terms of nutritional values, even in datasets exceeding millions of rows.

#### Data Preparation:

Nutritional data for each ingredient (e.g., energy, carb, protein, fat, sugar, water, fiber) was extracted and converted into feature vectors.

All feature vectors were normalized to ensure uniformity in the calculation of distances.

#### Index Construction:

The Faiss IndexFlatL2 algorithm was utilized, which computes approximate nearest neighbors based on Euclidean distance in high-dimensional space.

The feature vectors were added to the index, making it efficient to query for neighbors without requiring traditional training.

Substitution Recommendation:

For a given ingredient, its nutritional vector was compared to all other ingredient vectors in the index.

The top 2–3 nearest neighbors were selected as substitutes, based on their similarity scores (lower Euclidean distance implies higher similarity).

A similarity score, calculated as the distance metric, was also included in the results for transparency.

### API Response
The API provides a JSON response containing the original ingredient ID and a list of the most suitable substitute ingredients.

Example Response
```
{
  "ingredient_id": "ing_003",
  "substitutes": [
    {
      "id": "ing_003",
      "ingredient_name": "Heirloom Tomato",
      "similarity": 0
    },
    {
      "id": "ing_068",
      "ingredient_name": "Apple Cider Vinegar",
      "similarity": 22.8699951171875
    },
    {
      "id": "ing_013",
      "ingredient_name": "Fresh Lemon Juice",
      "similarity": 28.5699996948242
    }
  ]
}

```

A very simple database containing ingredients with nutrition information and recipes which use these ingredients.

The CSVs include:

- **Ingredient** — Contains ingredient details including nutrition, cost, and supplier
- **Nutrition** — A model to store nutritional values per 100g
- **RecipeIngredient** — Links ingredients to recipes with quantities
- **Recipe** — Contains a list of ingredients with their quantities

---

## Task 1: Cost & Nutrition API

Using **FastAPI**, build the following endpoints:

### `POST /recipes/`
- Create a new recipe.

### `GET /recipes/{id}/`
- Returns:
  - Recipe details
  - Total cost (based on quantity and ingredient cost)
  - Total nutrition (calculated by scaling `nutrition_per_100g` based on quantity used)

Example logic:
 python
total_cost = sum(ingredient.cost_per_gram * quantity for each ingredient)
nutrition = {
  "calories": sum(ingredient.nutrition["calories"] * quantity / 100 for each),
  ...
}

## Task 2: Suggest Ingredient Substitutes

### Add a basic substitute suggestion endpoint:
- **GET /ingredients/{id}/substitutes/**
  - Return 2-3 possible substitutes for an ingredient based on a similar nutrition profile (e.g., similar calories or macros).
  - Can be rule-based or use cosine similarity with Scikit-Learn.

### Optional Add-ons:
- Docker support
- Unit tests
- GitHub Actions CI

### **Submission Guidelines**
- Submit your code via GitHub or as a zip archive.
- Include a README with instructions to run your solution.
- Docker is optional but encouraged.
- Include basic tests if time allows.