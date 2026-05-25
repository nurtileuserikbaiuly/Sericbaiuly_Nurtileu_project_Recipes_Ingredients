import json
from part1 import Ingredient, Dish

class RecipeBook:
    def __init__(self):
        self.dishes = {}

    def add_dish(self, dish):
        self.dishes[dish.name] = dish

    def get_ingredients_gen(self, dish_name):
        dish = self.dishes.get(dish_name)
        if dish is None:
            return
        for ing in dish.ingredients:
            yield ing

    def high_calorie_ingredients(self, dish_name, limit=200):
        dish = self.dishes.get(dish_name)
        if dish is None:
            return []
        return [ing for ing in dish.ingredients if ing.cals_per_100g > limit]

    def sorted_by_calories(self, dish_name):
        dish = self.dishes.get(dish_name)
        if dish is None:
            return []
        return sorted(dish.ingredients, key=lambda ing: ing.total_calories(), reverse=True)

    def calorie_summary(self):
        return {
            name: sum(ing.total_calories() for ing in dish.ingredients)
            for name, dish in self.dishes.items()
        }
    def get_dish(self, name):
        return self.dishes.get(name)

    def all_names(self):
        return list(self.dishes.keys())

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

class BaseRecipe:

    def __init__(self, name, category):
        self.name = name
        self.category = category

    def describe(self):
        return f"[{self.category}] {self.name}"


class KazakhDish(BaseRecipe):

    def __init__(self, name):
        super().__init__(name, "Қазақ тағамы")
        self.ingredients = []

    def add_ingredient(self, ingredient):
        self.ingredients.append(ingredient)

    def total_weight(self):
        return sum(ing.grams for ing in self.ingredients)

    def total_calories(self):
        return sum(ing.total_calories() for ing in self.ingredients)

    def describe(self):
        base = super().describe()
        return f"{base} | {self.total_weight()}г | {self.total_calories():.0f} ккал"

    def __iter__(self):
        return iter(self.ingredients)


if __name__ == "__main__":

    beshbarmak = KazakhDish("Бешбармақ")
    beshbarmak.add_ingredient(Ingredient("Сиыр еті", 500, 187))
    beshbarmak.add_ingredient(Ingredient("Жайма", 300, 337))
    beshbarmak.add_ingredient(Ingredient("Пияз", 100, 41))

    manty = KazakhDish("Манты")
    manty.add_ingredient(Ingredient("Қой еті", 400, 209))
    manty.add_ingredient(Ingredient("Ұн", 250, 364))
    manty.add_ingredient(Ingredient("Пияз", 150, 41))

    print("Бешбармақ ингредиенттері (for арқылы):")
    for ing in beshbarmak:
        print(f"  {ing.name}: {ing.grams}г")

    book = RecipeBook()
    simple_besh = Dish("Бешбармақ")
    for ing in beshbarmak:
        simple_besh.add_ingredient(ing)

    simple_manty = Dish("Манты")
    for ing in manty:
        simple_manty.add_ingredient(ing)

    book.add_dish(simple_besh)
    book.add_dish(simple_manty)

    print("Генератор арқылы ингредиенттер:")
    for ing in book.get_ingredients_gen("Бешбармақ"):
        print(f"  {ing}")

    print("\nКалориясы жоғары ингредиенттер (>200 ккал/100г):")
    print(book.high_calorie_ingredients("Бешбармақ"))

    print("\nКалориясы бойынша сұрыпталған:")
    for ing in book.sorted_by_calories("Манты"):
        print(f"  {ing.name}: {ing.total_calories():.1f} ккал")

    print("\nТағамдар калориясы (dict comprehension):")
    print(book.calorie_summary())

    print(beshbarmak.describe())
    print(manty.describe())
