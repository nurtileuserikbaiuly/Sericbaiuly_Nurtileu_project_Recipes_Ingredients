class Ingredient:

    def __init__(self, name, grams, kcal_per_100g):
        self.name = name
        self.grams = grams
        self.kcal_per_100g = kcal_per_100g

    def get_calories(self):
        return (self.grams * self.kcal_per_100g) / 100

    def to_dict(self):
        return {
            "аты": self.name,
            "граммы": self.grams,
            "ккал/100г": self.kcal_per_100g,
            "жалпы_ккал": round(self.get_calories(), 2)
        }

    def __str__(self):
        return f" - {self.name}: {self.grams}г ({self.get_calories():.1f} ккал)"


class Dish:
    def __init__(self, dish_name):
        self.dish_name = dish_name
        self.ingredients = []

    def add_ingredient(self, ingredient):
        self.ingredients.append(ingredient)
        print(f"'{ingredient.name}' ингредиенті '{self.dish_name}' тағамына қосылды")

    def get_total_grams(self):
        total = 0
        for ing in self.ingredients:
            total += ing.grams
        return total

    def get_total_calories(self):
        total = 0
        for ing in self.ingredients:
            total += ing.get_calories()
        return total

    def show_info(self):
        print(f"\n  Тағам: {self.dish_name}")
        print(f"  Ингредиенттер ({len(self.ingredients)} дана):")
        for ing in self.ingredients:
            print(ing)
        print(f"  Жалпы салмақ : {self.get_total_grams()}г")
        print(f"  Жалпы калория: {self.get_total_calories():.1f} ккал")

    def to_dict(self):
        return {
            "тағам": self.dish_name,
            "ингредиенттер": [ing.to_dict() for ing in self.ingredients],
            "жалпы_грамм": self.get_total_grams(),
            "жалпы_ккал": round(self.get_total_calories(), 2)
        }


if __name__ == "__main__":

    beshbarmak = Dish("Бешбармақ")

    beshbarmak.add_ingredient(Ingredient("Қой еті",    500, 294))
    beshbarmak.add_ingredient(Ingredient("Жайма",      300, 337))
    beshbarmak.add_ingredient(Ingredient("Картоп",     200, 77))
    beshbarmak.add_ingredient(Ingredient("Пияз",        80, 41))
    beshbarmak.add_ingredient(Ingredient("Тұз",         10, 0))

    beshbarmak.show_info()