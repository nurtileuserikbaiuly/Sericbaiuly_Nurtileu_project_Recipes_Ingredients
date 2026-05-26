import pandas as pd
from part1 import Ingredient, Dish


class RecipeBook:
    def __init__(self):
        self.dishes = {}

    def add_dish(self, dish):
        self.dishes[dish.name] = dish

    def to_dataframe(self):
        rows = []
        for dish_name, dish in self.dishes.items():
            for ing in dish.ingredients:
                rows.append({
                    "тағам": dish_name,
                    "ингредиент": ing.name,
                    "граммдар": ing.grams,
                    "жалпы_ккал": ing.total_calories()
                })
        return pd.DataFrame(rows)

    def groupby_summary(self):
        df = self.to_dataframe()
        return df.groupby("тағам").agg(
            жалпы_граммдар=("граммдар", "sum"),
            жалпы_ккал=("жалпы_ккал", "sum"),
            ингредиент_саны=("ингредиент", "count")
        ).reset_index()


if __name__ == "__main__":
    book = RecipeBook()

    beshbarmak = Dish("Бешбармақ")
    beshbarmak.add_ingredient(Ingredient("Сиыр еті", 500, 187))
    beshbarmak.add_ingredient(Ingredient("Жайма", 300, 337))
    beshbarmak.add_ingredient(Ingredient("Пияз", 100, 41))

    manty = Dish("Манты")
    manty.add_ingredient(Ingredient("Қой еті", 400, 209))
    manty.add_ingredient(Ingredient("Ұн", 250, 364))
    manty.add_ingredient(Ingredient("Май", 30, 900))

    sorpa = Dish("Қой сорпасы")
    sorpa.add_ingredient(Ingredient("Қой еті", 600, 209))
    sorpa.add_ingredient(Ingredient("Картоп", 200, 77))
    sorpa.add_ingredient(Ingredient("Сәбіз", 100, 41))

    book.add_dish(beshbarmak)
    book.add_dish(manty)
    book.add_dish(sorpa)

    print("GroupBy қорытындысы:")
    print(book.groupby_summary().to_string(index=False))