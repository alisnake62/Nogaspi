from nogaspi.views.food.getAllergens import Allergen

def test_allergen_toJson():
    assert Allergen("English", "French").toJson() == "French"
    assert Allergen("English").toJson() == "English"