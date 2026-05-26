import json
from part1 import Ingredient, Dish
from Part2 import RecipeBook


class RecipeBookExtended(RecipeBook):

    def get_ingredients_gen(self, dish_name):
        dish = self.dishes.get(dish_name)
        if dish is None:
            return
        for ing in dish.ingredients:
            yield ing

    def export_to_json(self, dish_name):
        dish = self.dishes.get(dish_name)
        if dish is None:
            return None
        return json.dumps(dish.to_dict(), ensure_ascii=False, indent=2)


if __name__ == "__main__":
    book = RecipeBookExtended()

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

    print("Генератор арқылы ингредиенттер:")
    for ing in book.get_ingredients_gen("Бешбармақ"):
        print(f"  {ing}")

    print("\nJSON экспорт:")
    print(book.export_to_json("Манты"))