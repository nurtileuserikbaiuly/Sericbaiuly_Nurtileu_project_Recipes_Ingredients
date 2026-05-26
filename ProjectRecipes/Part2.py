from part1 import Ingredient, Dish


class RecipeBook:
    def __init__(self):
        self.dishes = {}

    def add_dish(self, dish):
        self.dishes[dish.name] = dish

    def get_dish(self, name):
        return self.dishes.get(name)

    def all_names(self):
        return list(self.dishes.keys())

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
        return {name: dish.total_calories() for name, dish in self.dishes.items()}


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

    book.add_dish(beshbarmak)
    book.add_dish(manty)

    print("Барлық тағамдар:", book.all_names())
    print("Калориясы жоғары ингредиенттер:", book.high_calorie_ingredients("Бешбармақ"))
    print("Сұрыпталған:", book.sorted_by_calories("Манты"))
    print("Калория қорытындысы:", book.calorie_summary())