import numpy as np
import json
from part1 import Ingredient, Dish
from Part2 import RecipeBook


class KazakhDish(Dish):
    def __init__(self, dish_name, region):
        super().__init__(dish_name)
        self.region = region

    def show_info(self):
        print(f"\nҚазақ тағамы: {self.dish_name}  [Аймақ: {self.region}]")
        print(f"  Ингредиенттер ({len(self.ingredients)} дана):")
        for ing in self.ingredients:
            print(ing)
        print(f"  Жалпы салмақ : {self.get_total_grams()}г")
        print(f"  Жалпы калория: {self.get_total_calories():.1f} ккал")

    def __del__(self):
        print(f"  '{self.dish_name}' объектісі жадтан өшірілді")


class VegetarianDish(Dish):
    MEAT_WORDS = ["ет", "балық", "тауық", "сиыр", "қой", "шошқа"]

    def __init__(self, dish_name):
        super().__init__(dish_name)

    def add_ingredient(self, ingredient):
        name_lower = ingredient.name.lower()
        for meat in self.MEAT_WORDS:
            if meat in name_lower:
                print(f"'{ingredient.name}' — вегетариандық тағамға ет қосуға болмайды!")
                return
        super().add_ingredient(ingredient)

    def show_info(self):
        print(f"\nВегетариандық тағам: {self.dish_name}")
        print(f"  Ингредиенттер ({len(self.ingredients)} дана):")
        for ing in self.ingredients:
            print(ing)
        print(f"  Жалпы салмақ : {self.get_total_grams()}г")
        print(f"  Жалпы калория: {self.get_total_calories():.1f} ккал")

    def __del__(self):
        print(f"'{self.dish_name}' (вег.) объектісі жадтан өшірілді")


class NumpyRecipeAnalyzer:
    def __init__(self, recipe_book):
        self.recipe_book = recipe_book
        self.grams_array    = None
        self.kcal_array     = None
        self.calories_array = None
        self.names_array    = None
        self._build_arrays()

    def _build_arrays(self):
        grams_list    = []
        kcal_list     = []
        names_list    = []

        for dish in self.recipe_book.dishes:
            for ing in dish.ingredients:
                grams_list.append(ing.grams)
                kcal_list.append(ing.kcal_per_100g)
                names_list.append(ing.name)

        self.grams_array    = np.array(grams_list,  dtype=np.float64)
        self.kcal_array     = np.array(kcal_list,   dtype=np.float64)
        self.names_array    = np.array(names_list)

        self.calories_array = (self.grams_array * self.kcal_array) / 100

    def basic_stats(self):
        return {
            "ингредиент_саны"    : len(self.grams_array),
            "орташа_грамм"       : round(float(np.mean(self.grams_array)),   1),
            "ең_көп_грамм"       : round(float(np.max(self.grams_array)),    1),
            "ең_аз_грамм"        : round(float(np.min(self.grams_array)),    1),
            "жалпы_калория_сумма": round(float(np.sum(self.calories_array)), 1),
            "орташа_калория"     : round(float(np.mean(self.calories_array)),1),
            "стандарт_ауытқу"    : round(float(np.std(self.calories_array)), 1),
        }

    def top_by_calories(self, top_n=5):
        sorted_indices = np.argsort(self.calories_array)[::-1]
        top_indices    = sorted_indices[:top_n]

        result = []
        for i in top_indices:
            result.append({
                "аты"        : self.names_array[i],
                "граммы"     : float(self.grams_array[i]),
                "жалпы_ккал" : round(float(self.calories_array[i]), 1)
            })
        return result

    def calories_by_dish(self):
        result = {}
        for dish in self.recipe_book.dishes:
            g = np.array([ing.grams        for ing in dish.ingredients], dtype=np.float64)
            k = np.array([ing.kcal_per_100g for ing in dish.ingredients], dtype=np.float64)

            total = float(np.sum((g * k) / 100))
            result[dish.dish_name] = round(total, 1)
        return result

    def show_numpy_stats(self):
        stats = self.basic_stats()
        for key, val in stats.items():
            print(f"  {key:<25}: {val}")

        print("\n Ең калориялы ТОП-5 ингредиент:")
        for i, item in enumerate(self.top_by_calories(5), start=1):
            print(f"  {i}. {item['аты']:<20} {item['граммы']:>5.0f}г  →  {item['жалпы_ккал']:>7.1f} ккал")

        print("\n Тағам бойынша жалпы калория (NumPy):")
        for dish_name, kcal in self.calories_by_dish().items():
            print(f"  {dish_name:<15}: {kcal:>8.1f} ккал")

class JsonExporter:
    def __init__(self, recipe_book):
        self.recipe_book = recipe_book

    def save(self, filename="рецепттер.json"):
        data = {
            "кітапхана"   : self.recipe_book.book_name,
            "тағамдар_саны": len(self.recipe_book),
            "рецепттер"   : [dish.to_dict() for dish in self.recipe_book.dishes]
        }
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"'{filename}' файлына {len(self.recipe_book)} тағам жазылды")
        return filename

    def load(self, filename="рецепттер.json"):
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        book = RecipeBook(data["кітапхана"] + " [жүктелген]")
        for d in data["рецепттер"]:
            dish = Dish(d["тағам"])
            for ing in d["ингредиенттер"]:
                dish.ingredients.append(Ingredient(ing["аты"], ing["граммы"], ing["ккал/100г"]))
            book.dishes.append(dish)

        print(f"'{filename}' файлынан {len(book)} тағам жүктелді")
        return book

def build_recipe_book():
    book = RecipeBook("Қазақ Тағамдары")
    book.create_and_add("Бешбармақ", [
        ("Қой еті",   500, 294), ("Жайма",  300, 337),
        ("Картоп",    200,  77), ("Пияз",    80,  41), ("Тұз", 10, 0),
    ])
    book.create_and_add("Манты", [
        ("Сиыр еті",  400, 187), ("Пияз",   150,  41),
        ("Бидай ұны", 350, 364), ("Тұз",     10,   0), ("Бұрыш", 5, 251),
    ])
    book.create_and_add("Плов", [
        ("Күріш",        400, 344), ("Сиыр еті",     300, 187),
        ("Сәбіз",        200,  35), ("Пияз",         150,  41),
        ("Өсімдік майы",  80, 884), ("Тұз",           10,   0),
    ])
    book.create_and_add("Лагман", [
        ("Сиыр еті",      350, 187), ("Лапша",        300, 337),
        ("Болгар бұрышы", 100,  27), ("Қызанақ",      150,  18),
        ("Пияз",          100,  41), ("Тұз",           10,   0),
    ])
    book.create_and_add("Самса", [
        ("Бидай ұны", 400, 364), ("Қой еті", 300, 294),
        ("Пияз",      150,  41), ("Май",      50, 717), ("Тұз", 10, 0),
    ])
    return book


if __name__ == "__main__":

    print("\n▶ KazakhDish (мұрагерлік):")
    besh = KazakhDish("Бешбармақ", "Солтүстік Қазақстан")
    besh.add_ingredient(Ingredient("Қой еті", 500, 294))
    besh.add_ingredient(Ingredient("Жайма",   300, 337))
    besh.add_ingredient(Ingredient("Картоп",  200,  77))
    besh.show_info()

    print("\n▶ VegetarianDish (инкапсуляция + мұрагерлік):")
    veg = VegetarianDish("Көкөніс сорпасы")
    veg.add_ingredient(Ingredient("Картоп",  200, 77))
    veg.add_ingredient(Ingredient("Сиыр еті", 300, 187))  # блокталу керек!
    veg.add_ingredient(Ingredient("Сәбіз",   150, 35))
    veg.add_ingredient(Ingredient("Пияз",    100, 41))
    veg.show_info()

    print("\n▶ Полиморфизм — бір цикл, екі түрлі нәтиже:")
    dishes_list = [
        KazakhDish("Манты", "Оңтүстік"),
        VegetarianDish("Жемістер салаты"),
    ]
    dishes_list[0].add_ingredient(Ingredient("Сиыр еті",  400, 187))
    dishes_list[0].add_ingredient(Ingredient("Бидай ұны", 350, 364))
    dishes_list[1].add_ingredient(Ingredient("Алма",  150, 52))
    dishes_list[1].add_ingredient(Ingredient("Банан", 120, 89))

    for dish in dishes_list:
        dish.show_info()

    print("\n▶ NumPy талдауы:")
    book = build_recipe_book()
    analyzer = NumpyRecipeAnalyzer(book)
    analyzer.show_numpy_stats()

    print("\n▶ JSON экспорты:")
    exporter = JsonExporter(book)
    exporter.save("рецепттер.json")
    loaded = exporter.load("рецепттер.json")
    print(f"  Жүктелген тағамдар: {len(loaded)}")
