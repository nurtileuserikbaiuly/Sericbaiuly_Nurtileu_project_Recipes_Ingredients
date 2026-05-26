class Ingredient:
    def __init__(self, name, grams, cals_per_100g):
        self.name = name
        self.grams = grams
        self.cals_per_100g = cals_per_100g

    def total_calories(self):
        return (self.grams * self.cals_per_100g) / 100

    def to_dict(self):
        return {
            "name": self.name,
            "grams": self.grams,
            "cals_per_100g": self.cals_per_100g,
            "total_calories": self.total_calories()
        }

    def __repr__(self):
        return f"{self.name}: {self.grams}г, {self.total_calories():.1f} ккал"


class Dish:
    def __init__(self, name):
        self.name = name
        self.ingredients = []

    def add_ingredient(self, ingredient):
        self.ingredients.append(ingredient)

    def total_weight(self):
        return sum(ing.grams for ing in self.ingredients)

    def total_calories(self):
        return round(sum(ing.total_calories() for ing in self.ingredients), 1)

    def to_dict(self):
        return {
            "name": self.name,
            "total_weight": self.total_weight(),
            "total_calories": self.total_calories(),
            "ingredients": [ing.to_dict() for ing in self.ingredients]
        }

    def __repr__(self):
        return f"{self.name} | {self.total_weight()}г | {self.total_calories()} ккал"


if __name__ == "__main__":
    beshbarmak = Dish("Бешбармақ")
    beshbarmak.add_ingredient(Ingredient("Сиыр еті", 500, 187))
    beshbarmak.add_ingredient(Ingredient("Жайма", 300, 337))
    beshbarmak.add_ingredient(Ingredient("Пияз", 100, 41))

    for ing in beshbarmak.ingredients:
        print(ing)

    print(beshbarmak)