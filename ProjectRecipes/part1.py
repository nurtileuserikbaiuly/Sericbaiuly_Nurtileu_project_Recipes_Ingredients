class Ingredient:
    def __init__(self, name, grams, cals_per_100g):
        self.name = name
        self.grams = grams
        self.cals_per_100g = cals_per_100g

    def total_calories(self):
        return (self.grams * self.cals_per_100g) / 100

    def to_string(self):
        return f"{self.name}: {self.grams}г, {self.total_calories():.1f} ккал"


class Dish:

    def __init__(self, name):
        self.name = name
        self.ingredients = []

    def add_ingredient(self, ingredient):
        self.ingredients.append(ingredient)

    def ingredient_names(self):
        return [ing.name for ing in self.ingredients]

    def summary(self):
        total = sum(ing.total_calories() for ing in self.ingredients)
        weight = sum(ing.grams for ing in self.ingredients)
        return f"Тағам: {self.name} | Салмақ: {weight}г | Калория: {total:.1f} ккал"


class RecipeStorage:

    def __init__(self):
        self.recipes = {}

    def add(self, dish):
        self.recipes[dish.name] = dish

    def get(self, name):
        return self.recipes.get(name, None)

    def all_names(self):
        return list(self.recipes.keys())

    def ingredient_dict(self, dish_name):
        dish = self.get(dish_name)
        if dish is None:
            return {}
        return {ing.name: ing.grams for ing in dish.ingredients}


class FileManager:

    def __init__(self, filename="recipes.txt"):
        self.filename = filename

    def save(self, storage):
        with open(self.filename, "w", encoding="utf-8") as f:
            for name, dish in storage.recipes.items():
                f.write(f"ТАҒАМ: {name}\n")
                for ing in dish.ingredients:
                    f.write(f"  {ing.name},{ing.grams},{ing.cals_per_100g}\n")
                f.write("\n")

    def load(self):
        storage = RecipeStorage()
        current_dish = None
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.rstrip()
                    if line.startswith("ТАҒАМ:"):
                        name = line.replace("ТАҒАМ:", "").strip()
                        current_dish = Dish(name)
                        storage.add(current_dish)
                    elif line.startswith("  ") and current_dish:
                        parts = line.strip().split(",")
                        ing = Ingredient(parts[0], float(parts[1]), float(parts[2]))
                        current_dish.add_ingredient(ing)
        except FileNotFoundError:
            print("Файл табылмады.")
        return storage

    def print_file(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                print(f.read())
        except FileNotFoundError:
            print("Файл жоқ.")
if __name__ == "__main__":

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

    for ing in beshbarmak.ingredients:
        print(ing.to_string())

    print("\nИнгредиент атаулары тізімі:")
    print(beshbarmak.ingredient_names())

    print("\n" + beshbarmak.summary())
    print(manty.summary())

    storage = RecipeStorage()
    storage.add(beshbarmak)
    storage.add(manty)

    print("Барлық рецепттер:", storage.all_names())
    print("Бешбармақ ингредиенттері (сөздік):")
    print(storage.ingredient_dict("Бешбармақ"))


    fm = FileManager("recipes.txt")
    fm.save(storage)
    print("Файлға жазылды: recipes.txt")

    print("\nФайл мазмұны:")
    fm.print_file()

    print("Файлдан оқу:")
    loaded = fm.load()
    for name in loaded.all_names():
        dish = loaded.get(name)
        print(dish.summary())
