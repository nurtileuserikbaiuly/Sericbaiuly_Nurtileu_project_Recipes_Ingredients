import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from part1 import Ingredient, Dish
matplotlib.use("Agg")



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
                    "ккал_100г": ing.cals_per_100g,
                    "жалпы_ккал": ing.total_calories()
                })
        return pd.DataFrame(rows)

    def groupby_summary(self):
        df = self.to_dataframe()
        summary = df.groupby("тағам").agg(
            жалпы_граммдар=("граммдар", "sum"),
            жалпы_ккал=("жалпы_ккал", "sum"),
            ингредиент_саны=("ингредиент", "count")
        ).reset_index()
        return summary

    def dish_dataframe(self, dish_name):
        df = self.to_dataframe()
        return df[df["тағам"] == dish_name].reset_index(drop=True)



class ChartBuilder:

    def bar_chart_weight(self, book, dish_name, save_path="bar_weight.png"):
        df = book.dish_dataframe(dish_name)

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar(df["ингредиент"], df["граммдар"], color="steelblue")
        ax.set_title(f"{dish_name} — ингредиент салмақтары")
        ax.set_xlabel("Ингредиент")
        ax.set_ylabel("Граммдар")
        ax.tick_params(axis="x", rotation=30)
        plt.tight_layout()
        plt.savefig(save_path)
        plt.close()
        print(f"Диаграмма сақталды: {save_path}")

    def bar_chart_calories(self, book, dish_name, save_path="bar_calories.png"):
        df = book.dish_dataframe(dish_name)

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar(df["ингредиент"], df["жалпы_ккал"], color="tomato")
        ax.set_title(f"{dish_name} — ингредиент калориялары")
        ax.set_xlabel("Ингредиент")
        ax.set_ylabel("Калория (ккал)")
        ax.tick_params(axis="x", rotation=30)
        plt.tight_layout()
        plt.savefig(save_path)
        plt.close()
        print(f"Диаграмма сақталды: {save_path}")

    def comparison_chart(self, book, save_path="comparison.png"):
        summary = book.groupby_summary()

        fig, axes = plt.subplots(1, 2, figsize=(12, 5))

        axes[0].bar(summary["тағам"], summary["жалпы_граммдар"], color="steelblue")
        axes[0].set_title("Жалпы салмақ (г)")
        axes[0].set_ylabel("Граммдар")
        axes[0].tick_params(axis="x", rotation=20)

        axes[1].bar(summary["тағам"], summary["жалпы_ккал"], color="tomato")
        axes[1].set_title("Жалпы калория (ккал)")
        axes[1].set_ylabel("Калория")
        axes[1].tick_params(axis="x", rotation=20)

        plt.suptitle("Тағамдар салыстырмасы")
        plt.tight_layout()
        plt.savefig(save_path)
        plt.close()
        print(f"Диаграмма сақталды: {save_path}")


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

    sorpa = Dish("Қой сорпасы")
    sorpa.add_ingredient(Ingredient("Қой еті", 600, 209))
    sorpa.add_ingredient(Ingredient("Картоп", 200, 77))
    sorpa.add_ingredient(Ingredient("Сәбіз", 100, 41))
    sorpa.add_ingredient(Ingredient("Пияз", 100, 41))

    book = RecipeBook()
    book.add_dish(beshbarmak)
    book.add_dish(manty)
    book.add_dish(sorpa)


    df = book.to_dataframe()
    print("Толық DataFrame:")
    print(df.to_string(index=False))

    print("\nGroupBy қорытындысы (тағам бойынша):")
    summary = book.groupby_summary()
    print(summary.to_string(index=False))

    print("\nБешбармақ DataFrame:")
    print(book.dish_dataframe("Бешбармақ").to_string(index=False))

    print("\nКалориясы 100-ден жоғары ингредиенттер:")
    high = df[df["жалпы_ккал"] > 100][["тағам", "ингредиент", "жалпы_ккал"]]
    print(high.to_string(index=False))


    charts = ChartBuilder()
    charts.bar_chart_weight(book, "Бешбармақ", "bar_weight.png")
    charts.bar_chart_calories(book, "Манты", "bar_calories.png")
    charts.comparison_chart(book, "comparison.png")
