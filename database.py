import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import faiss

# Đọc dữ liệu CSV
ingredients_df = pd.read_csv("sample-data/ingredients.csv")
recipes_df = pd.read_csv("sample-data/recipes.csv")
# Chỉ lấy các giá trị dinh dưỡng để làm vector đặc trưng
nutrition_features = ingredients_df[["energy", "carb", "protein", "fat", "sugar", "water", "fiber"]].values
nutrition_features = np.array(nutrition_features, dtype='float32')  # Faiss yêu cầu dữ liệu kiểu float32

# Xây dựng index ANN bằng Faiss
dimension = nutrition_features.shape[1]  # Số chiều của dữ liệu
index = faiss.IndexFlatL2(dimension)  # Sử dụng khoảng cách Euclidean (L2)
index.add(nutrition_features)  # Thêm dữ liệu vào index

print(f"Number of elements in index: {index.ntotal}")

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

# Hàm tìm nguyên liệu thay thế
def find_nearest_neighbors(ingredient_id: str, k: int = 3):
    # Tìm vector của nguyên liệu đầu vào
    target_row = ingredients_df[ingredients_df["id"] == ingredient_id]
    if target_row.empty:
        return None
    
    target_vector = target_row[["energy", "carb", "protein", "fat", "sugar", "water", "fiber"]].values
    target_vector = np.array(target_vector, dtype='float32').reshape(1, -1)

    # Tìm k nguyên liệu gần nhất
    distances, indices = index.search(target_vector, k)
    
    # Trả về danh sách các nguyên liệu thay thế
    substitutes = []
    for i, idx in enumerate(indices[0]):
        ingredient = ingredients_df.iloc[idx]
        substitutes.append({
            "id": ingredient["id"],
            "ingredient_name": ingredient["ingredient_name"],
            "similarity": float(distances[0][i])  # Chuyển đổi numpy.float32 -> float
        })
    
    return substitutes