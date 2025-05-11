import pytest
import requests

BASE_URL = "http://localhost:8000"

@pytest.mark.parametrize("ingredientes", [
    ["bacon", "apple", "almond butter"],
    ["artichoke cooked", "american cheese", "apple pie"],
    ["bagel", "almonds raw", "avocado", "adzuki beans cooked"],
])

def test_predict_endpoint(ingredientes):
    response = requests.post(f"{BASE_URL}/predict", json={"ingredientes": ingredientes})
    
    assert response.status_code == 200, f"Erro na API: {response.text}"
    
    data = response.json()
    assert "classificacao" in data
    assert "probabilidade" in data
    assert "detalhes_nutricionais" in data
    assert isinstance(data["classificacao"], int)
    assert isinstance(data["probabilidade"], float)
