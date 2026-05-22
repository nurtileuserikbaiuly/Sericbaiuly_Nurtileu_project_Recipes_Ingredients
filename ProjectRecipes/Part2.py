from part1 import Ingredient, Dish


def print_separator(title=""):
    print("\n" + "─" * 50)
    if title:
        print(f"  {title}")
        print("─" * 50)


class RecipeBook:
    def __init__(self, book_name):
        self.book_name = book_name
        self.dishes = []

    def add_dish(self, dish):
        if self.find_dish(dish.dish_name):
            print(f"'{dish.dish_name}' тағамы кітапханада бар!")
            return

        self.dishes.append(dish)
        print(f"'{dish.dish_name}' тағамы кітапханаға қосылды")

    def create_and_add(self, dish_name, ingredients_data):
        new_dish = Dish(dish_name)
        for name, grams, kcal in ingredients_data:
            new_dish.add_ingredient(Ingredient(name, grams, kcal))
        self.add_dish(new_dish)
        return new_dish

    def remove_dish(self, dish_name):
        dish = self.find_dish(dish_name)
        if dish:
            self.dishes.remove(dish)
            print(f"'{dish_name}' тағамы жойылды")
        else:
            print(f" '{dish_name}' табылмады!")


    def find_dish(self, dish_name):
        for dish in self.dishes:
            if dish.dish_name == dish_name:
                return dish
        return None

    def find_by_ingredient(self, ingredient_name):
        result = []
        for dish in self.dishes:
            for ing in dish.ingredients:
                if ingredient_name.lower() in ing.name.lower():
                    result.append(dish)
                    break
        return result

    def show_all(self):
        print_separator(f" {self.book_name} — барлық тағамдар")

        if not self.dishes:
            print("  Кітапхана бос!")
            return

        for i, dish in enumerate(self.dishes, start=1):
            print(f"\n  {i}. {dish.dish_name}")
            print(f"     Ингредиент саны : {len(dish.ingredients)}")
            print(f"     Жалпы салмақ    : {dish.get_total_grams()}г")
            print(f"     Жалпы калория   : {dish.get_total_calories():.1f} ккал")

    def show_dish_details(self, dish_name):
        dish = self.find_dish(dish_name)
        if dish:
            dish.show_info()
        else:
            print(f"'{dish_name}' тағамы табылмады!")

    def get_stats(self):
        if not self.dishes:
            return {}

        total_dishes = len(self.dishes)
        total_ingredients = sum(len(d.ingredients) for d in self.dishes)
        avg_calories = sum(d.get_total_calories() for d in self.dishes) / total_dishes

        most_caloric = max(self.dishes, key=lambda d: d.get_total_calories())
        least_caloric = min(self.dishes, key=lambda d: d.get_total_calories())

        return {
            "тағамдар_саны": total_dishes,
            "жалпы_ингредиенттер": total_ingredients,
            "орташа_калория": round(avg_calories, 1),
            "ең_калориялы": most_caloric.dish_name,
            "ең_аз_калориялы": least_caloric.dish_name
        }

    def show_stats(self):
        stats = self.get_stats()
        if not stats:
            print("Деректер жоқ!")
            return

        print_separator("Кітапхана статистикасы")
        print(f"  Тағамдар саны         : {stats['тағамдар_саны']}")
        print(f"  Жалпы ингредиенттер   : {stats['жалпы_ингредиенттер']}")
        print(f"  Орташа калория        : {stats['орташа_калория']} ккал")
        print(f"  Ең калориялы тағам    : {stats['ең_калориялы']}")
        print(f"  Ең аз калориялы тағам : {stats['ең_аз_калориялы']}")

    def __len__(self):
        return len(self.dishes)

    def __str__(self):
        return f"RecipeBook('{self.book_name}', тағамдар: {len(self.dishes)})"

if __name__ == "__main__":
    book = RecipeBook("Қазақ Тағамдары")

    book.create_and_add("Бешбармақ", [
        ("Қой еті", 500, 294),
        ("Жайма", 300, 337),
        ("Картоп", 200, 77),
        ("Пияз", 80, 41),
        ("Тұз", 10, 0),
    ])

    book.create_and_add("Манты", [
        ("Сиыр еті", 400, 187),
        ("Пияз", 150, 41),
        ("Бидай ұны", 350, 364),
        ("Тұз", 10, 0),
        ("Бұрыш", 5, 251),
    ])

    book.create_and_add("Плов", [
        ("Күріш", 400, 344),
        ("Сиыр еті", 300, 187),
        ("Сәбіз", 200, 35),
        ("Пияз", 150, 41),
        ("Өсімдік майы", 80, 884),
        ("Тұз", 10, 0),
    ])

    book.create_and_add("Лагман", [
        ("Сиыр еті", 350, 187),
        ("Лапша", 300, 337),
        ("Болгар бұрышы", 100, 27),
        ("Қызанақ", 150, 18),
        ("Пияз", 100, 41),
        ("Тұз", 10, 0),
    ])

    book.create_and_add("Самса", [
        ("Бидай ұны", 400, 364),
        ("Қой еті", 300, 294),
        ("Пияз", 150, 41),
        ("Май", 50, 717),
        ("Тұз", 10, 0),
    ])

    book.show_all()

    book.show_dish_details("Плов")

    book.show_stats()

    print_separator("'Пияз' бар тағамдар:")
    found = book.find_by_ingredient("Пияз")
    for d in found:
        print(f"  - {d.dish_name}")

    print()
    book.remove_dish("Лагман")
    print(f"Кітапханада қалған тағамдар: {len(book)}")