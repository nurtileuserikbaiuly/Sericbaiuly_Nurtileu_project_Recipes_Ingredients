from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import json
from part1 import Ingredient, Dish
from Part2 import RecipeBook



book = RecipeBook()

beshbarmak = Dish("Бешбармақ")
beshbarmak.add_ingredient(Ingredient("Сиыр еті", 500, 187))
beshbarmak.add_ingredient(Ingredient("Жайма", 300, 337))
beshbarmak.add_ingredient(Ingredient("Пияз", 100, 41))
beshbarmak.add_ingredient(Ingredient("Тұз", 10, 0))

manty = Dish("Манты")
manty.add_ingredient(Ingredient("Қой еті", 400, 209))
manty.add_ingredient(Ingredient("Ұн", 250, 364))
manty.add_ingredient(Ingredient("Пияз", 150, 41))
manty.add_ingredient(Ingredient("Май", 30, 900))

sorpa = Dish("Қой сорпасы")
sorpa.add_ingredient(Ingredient("Қой еті", 600, 209))
sorpa.add_ingredient(Ingredient("Картоп", 200, 77))
sorpa.add_ingredient(Ingredient("Сәбіз", 100, 41))

book.add_dish(beshbarmak)
book.add_dish(manty)
book.add_dish(sorpa)



class IngredientModel(BaseModel):
    name: str
    grams: float
    cals_per_100g: float


class DishModel(BaseModel):
    name: str
    ingredients: List[IngredientModel]



app = FastAPI(title="Рецепттер API", version="1.0")


@app.get("/")
def root():
    return {"хабарлама": "Рецепттер API іске қосылды"}

@app.get("/dishes")
def get_all_dishes():
    return {"тағамдар": book.all_names()}

@app.get("/dishes/{dish_name}")
def get_dish(dish_name: str):
    dish = book.get_dish(dish_name)
    if dish is None:
        raise HTTPException(status_code=404, detail="Тағам табылмады")
    return dish.to_dict()

@app.get("/dishes/{dish_name}/ingredients")
def get_ingredients(dish_name: str):
    dish = book.get_dish(dish_name)
    if dish is None:
        raise HTTPException(status_code=404, detail="Тағам табылмады")
    result = list(book.get_ingredients_gen(dish_name))
    return {"ингредиенттер": [ing.to_dict() for ing in result]}

@app.get("/dishes/{dish_name}/export")
def export_dish(dish_name: str):
    data = book.export_to_json(dish_name)
    if data is None:
        raise HTTPException(status_code=404, detail="Тағам табылмады")
    return json.loads(data)

@app.post("/dishes")
def add_dish(dish_model: DishModel):
    new_dish = Dish(dish_model.name)
    for ing_data in dish_model.ingredients:
        ing = Ingredient(ing_data.name, ing_data.grams, ing_data.cals_per_100g)
        new_dish.add_ingredient(ing)
    book.add_dish(new_dish)
    return {"хабарлама": f"'{dish_model.name}' қосылды", "тағам": new_dish.to_dict()}

@app.delete("/dishes/{dish_name}")
def delete_dish(dish_name: str):
    if dish_name not in book.dishes:
        raise HTTPException(status_code=404, detail="Тағам табылмады")
    del book.dishes[dish_name]
    return {"хабарлама": f"'{dish_name}' жойылды"}

if __name__ == "__main__":
    import uvicorn

    print("API іске қосылуда...")
    print("Swagger UI: http://127.0.0.1:8000/docs")
    print("Redoc: http://127.0.0.1:8000/redoc")
    print()
    print("Қолжетімді маршруттар:")
    print("  GET  /             — Қарсы алу")
    print("  GET  /dishes       — Барлық тағамдар")
    print("  GET  /dishes/{name}           — Бір тағам")
    print("  GET  /dishes/{name}/ingredients — Ингредиенттер")
    print("  GET  /dishes/{name}/export    — JSON экспорт")
    print("  POST /dishes       — Жаңа тағам қосу")
    print("  DELETE /dishes/{name}         — Тағамды жою")
    print()

    for ing in book.get_ingredients_gen("Бешбармақ"):
        print(f"  {ing.name}: {ing.grams}г")

    print(book.export_to_json("Манты"))

    uvicorn.run(app, host="0.0.0.0", port=8000)
