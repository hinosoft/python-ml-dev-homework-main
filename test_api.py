import sys
sys.path.append("..")  # Thêm thư mục cha vào sys.path
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Kiểm tra API lấy công thức theo ID
def test_get_recipe():
    response = client.get("/recipes/1/")
    assert response.status_code == 200
    data = response.json()
    assert "recipe" in data
    assert "total_cost" in data
    assert "nutrition" in data

# Kiểm tra API với ID không tồn tại
def test_invalid_recipe():
    response = client.get("/recipes/9999/")
    assert response.status_code == 404

# Kiểm tra API tạo công thức mới
def test_create_recipe():
    new_recipe = {
        "recipe_name": "Test Recipe",
        "recipe_type": "Soup",
        "cuisine": "Asian",
        "ingredients": [
            {"ingredient_id": "3", "ingredient_name": "Heirloom Tomato", "quantity_in_grams": 100},
            {"ingredient_id": "6", "ingredient_name": "Organic Spinach", "quantity_in_grams": 50}
        ]
    }

    response = client.post("/recipes/", json=new_recipe)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Recipe added successfully"
    assert data["recipe"]["recipe_name"] == "Test Recipe"

# Kiểm tra API tìm nguyên liệu thay thế
def test_find_substitutes_success():
    response = client.get("/ingredients/ing_003/substitutes/")
    assert response.status_code in [200, 404]  # Nếu có hoặc không có thay thế đều hợp lệ
    if response.status_code == 200:
        data = response.json()
        assert "substitutes" in data
        assert len(data["substitutes"]) > 0


# Kiểm tra API tìm nguyên liệu thay thế
def test_find_substitutes():
    response = client.get("/ingredients/3/substitutes/")
    assert response.status_code in [200, 404]  # Nếu có hoặc không có thay thế đều hợp lệ
    if response.status_code == 200:
        data = response.json()
        assert "substitutes" in data
        assert len(data["substitutes"]) > 0
        
# Kiểm tra API tìm nguyên liệu thay thế
def test_find_substitutes_success():
    response = client.get("/ingredients/ing_003/substitutes/")
    assert response.status_code in [200, 404]  # Nếu có hoặc không có thay thế đều hợp lệ
    if response.status_code == 200:
        data = response.json()
        assert "substitutes" in data
        assert len(data["substitutes"]) > 0


# Kiểm tra API tìm nguyên liệu thay thế
def test_find_substitutes():
    response = client.get("/ingredients/3/substitutes/")
    assert response.status_code in [200, 404]  # Nếu có hoặc không có thay thế đều hợp lệ
    if response.status_code == 200:
        data = response.json()
        assert "substitutes" in data
        assert len(data["substitutes"]) > 0
