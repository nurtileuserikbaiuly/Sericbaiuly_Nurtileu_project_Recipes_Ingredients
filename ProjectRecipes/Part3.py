import numpy as np
from part1 import Ingredient, Dish

class BaseRecipe:

    def __init__(self, name):
        self.name = name

    def describe(self):
        return f"Рецепт: {self.name}"

    def __del__(self):
        pass


class Dish(BaseRecipe):

    def __init__(self, name, cuisine="Қазақ"):
        super().__init__(name)
        self.cuisine = cuisine
        self.ingredients = []

    def add_ingredient(self, ingredient):
        self.ingredients.append(ingredient)

    def total_weight(self):
        return sum(ing.grams for ing in self.ingredients)

    def total_calories(self):
        return sum(ing.total_calories() for ing in self.ingredients)

    def describe(self):
        return (f"[{self.cuisine}] {self.name} | "
                f"{self.total_weight()}г | {self.total_calories():.0f} ккал")

    def __del__(self):
        pass


class SoupDish(Dish):

    def __init__(self, name, liters=1.0):
        super().__init__(name, cuisine="Қазақ сорпасы")
        self.liters = liters

    def describe(self):
        return f"{super().describe()} | {self.liters}л"



class NutritionAnalyzer:

    def __init__(self, dish):
        self.dish = dish
        self.weights = np.array([ing.grams for ing in dish.ingredients])
        self.cals_per_100 = np.array([ing.cals_per_100g for ing in dish.ingredients])
        self.names = [ing.name for ing in dish.ingredients]

    def calories_array(self):
        return (self.weights * self.cals_per_100) / 100

    def total_weight(self):
        return np.sum(self.weights)

    def total_calories(self):
        return np.sum(self.calories_array())

    def max_calorie_ingredient(self):
        idx = np.argmax(self.calories_array())
        return self.names[idx]

    def min_calorie_ingredient(self):
        idx = np.argmin(self.calories_array())
        return self.names[idx]

    def weight_percent(self):
        return np.round((self.weights / self.total_weight()) * 100, 1)

    def stats(self):
        cals = self.calories_array()
        return {
            "орташа_калория": round(float(np.mean(cals)), 1),
            "максимум": round(float(np.max(cals)), 1),
            "минимум": round(float(np.min(cals)), 1),
            "стандарт_ауытқу": round(float(np.std(cals)), 1),
        }



if __name__ == "__main__":


    beshbarmak = Dish("Бешбармақ")
    beshbarmak.add_ingredient(Ingredient("Сиыр еті", 500, 187))
    beshbarmak.add_ingredient(Ingredient("Жайма", 300, 337))
    beshbarmak.add_ingredient(Ingredient("Пияз", 100, 41))
    beshbarmak.add_ingredient(Ingredient("Тұз", 10, 0))

    sorpa = SoupDish("Қой сорпасы", liters=2.0)
    sorpa.add_ingredient(Ingredient("Қой еті", 600, 209))
    sorpa.add_ingredient(Ingredient("Сәбіз", 100, 41))
    sorpa.add_ingredient(Ingredient("Пияз", 100, 41))
    sorpa.add_ingredient(Ingredient("Картоп", 200, 77))

    dishes = [beshbarmak, sorpa]
    for d in dishes:
        print(d.describe())

    print("\nИнкапсуляция (getter арқылы):")
    ing = Ingredient("Тест", 100, 200)
    print(f"  Атау: {ing.name}, Граммдар: {ing.grams}, Калория/100г: {ing.cals_per_100g}")

    print("\nДеструктор тексеру:")
    temp = Dish("Уақытша тағам")
    print(f"  '{temp.name}' жасалды")
    del temp
    print("  Объект жойылды (__del__ іске қосылды)")

    analyzer = NutritionAnalyzer(beshbarmak)

    print(f"Тағам: {beshbarmak.name}")
    print(f"Жалпы салмақ: {analyzer.total_weight()}г")
    print(f"Жалпы калория: {analyzer.total_calories():.1f} ккал")
    print(f"Ең калориялы ингредиент: {analyzer.max_calorie_ingredient()}")
    print(f"Ең аз калориялы: {analyzer.min_calorie_ingredient()}")

    print("\nИнгредиент үлестері (%):")
    for name, pct in zip(analyzer.names, analyzer.weight_percent()):
        print(f"  {name}: {pct}%")

    print("\nСтатистика:")
    for k, v in analyzer.stats().items():
        print(f"  {k}: {v}")

    print(f"  Салмақтар массиві: {analyzer.weights}")
    print(f"  Калориялар массиві: {np.round(analyzer.calories_array(), 1)}")
    print(f"  Жалпы калория (np.dot): {np.dot(analyzer.weights, analyzer.cals_per_100) / 100:.1f} ккал")
