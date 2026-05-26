import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from part1 import Ingredient, Dish
from Part4 import RecipeBook



def bar_chart(book, dish_name, save_path="bar.png"):
    df = book.to_dataframe()
    dish_df = df[df["тағам"] == dish_name].reset_index(drop=True)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(dish_df["ингредиент"], dish_df["граммдар"], color="steelblue")
    ax.set_title(f"{dish_name} — ингредиент салмақтары")
    ax.set_xlabel("Ингредиент")
    ax.set_ylabel("Граммдар")
    ax.tick_params(axis="x", rotation=30)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()
    print(f"График сақталды: {save_path}")


book = RecipeBook()

beshbarmak = Dish("Бешбармақ")
beshbarmak.add_ingredient(Ingredient("Сиыр еті", 500, 187))
beshbarmak.add_ingredient(Ingredient("Жайма", 300, 337))
beshbarmak.add_ingredient(Ingredient("Пияз", 100, 41))

manty = Dish("Манты")
manty.add_ingredient(Ingredient("Қой еті", 400, 209))
manty.add_ingredient(Ingredient("Ұн", 250, 364))
manty.add_ingredient(Ingredient("Май", 30, 900))

book.add_dish(beshbarmak)
book.add_dish(manty)


class IngredientModel(BaseModel):
    name: str
    grams: float
    cals_per_100g: float


class DishModel(BaseModel):
    name: str
    ingredients: List[IngredientModel]


app = FastAPI(title="Рецепттер API", version="1.0")


@app.get("/dishes")
def get_all_dishes():
    return {"тағамдар": list(book.dishes.keys())}


@app.get("/dishes/{dish_name}")
def get_dish(dish_name: str):
    dish = book.dishes.get(dish_name)
    if dish is None:
        raise HTTPException(status_code=404, detail="Тағам табылмады")
    return dish.to_dict()


@app.post("/dishes")
def add_dish(dish_model: DishModel):
    new_dish = Dish(dish_model.name)
    for ing in dish_model.ingredients:
        new_dish.add_ingredient(Ingredient(ing.name, ing.grams, ing.cals_per_100g))
    book.add_dish(new_dish)
    return {"хабарлама": f"'{dish_model.name}' қосылды"}


@app.delete("/dishes/{dish_name}")
def delete_dish(dish_name: str):
    if dish_name not in book.dishes:
        raise HTTPException(status_code=404, detail="Тағам табылмады")
    del book.dishes[dish_name]
    return {"хабарлама": f"'{dish_name}' жойылды"}


if __name__ == "__main__":
    import uvicorn

    bar_chart(book, "Бешбармақ", "bar.png")

    print("Swagger UI: http://127.0.0.1:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)