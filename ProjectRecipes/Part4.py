import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from Part3 import build_recipe_book, NumpyRecipeAnalyzer


class NumpyAdvanced:
    def __init__(self, recipe_book):
        self.recipe_book = recipe_book
        self._build_matrix()

    def _build_matrix(self):
        rows = []
        self.dish_names = []
        for dish in self.recipe_book.dishes:
            g = np.array([i.grams         for i in dish.ingredients], dtype=np.float64)
            k = np.array([i.kcal_per_100g  for i in dish.ingredients], dtype=np.float64)
            rows.append([
                float(np.sum(g)),
                float(np.mean(k)),
                float(np.sum((g * k) / 100)),
            ])
            self.dish_names.append(dish.dish_name)

        self.matrix = np.array(rows, dtype=np.float64)

    def show_matrix(self):
        print("\n  NumPy 2D матрица (тағам × [граммы, орт.ккал/100г, жалпы_ккал]):")
        print(f"  Өлшем: {self.matrix.shape}")
        headers = ["жалпы_г", "орт.ккал/100г", "жалпы_ккал"]
        print(f"  {'Тағам':<15} " + "  ".join(f"{h:>14}" for h in headers))
        for name, row in zip(self.dish_names, self.matrix):
            print(f"  {name:<15} " + "  ".join(f"{v:>14.1f}" for v in row))

    def percentile_info(self):
        calories_col = self.matrix[:, 2]
        print("\n  Калория перцентильдері:")
        for p in [25, 50, 75]:
            val = np.percentile(calories_col, p)
            print(f"  {p}% перцентиль: {val:.1f} ккал")

    def where_example(self):
        calories_col = self.matrix[:, 2]
        mask   = np.where(calories_col > 2500)[0]
        result = [self.dish_names[i] for i in mask]
        print(f"\n  np.where: 2500+ ккал тағамдар: {result}")
        return result

class PandasAnalyzer:
    def __init__(self, recipe_book):
        self.recipe_book = recipe_book
        self.df = self._build_dataframe()

    def _build_dataframe(self):
        rows = []
        for dish in self.recipe_book.dishes:
            for ing in dish.ingredients:
                rows.append({
                    "тағам"     : dish.dish_name,
                    "ингредиент": ing.name,
                    "граммы"    : ing.grams,
                    "ккал_100г" : ing.kcal_per_100g,
                    "жалпы_ккал": round(ing.get_calories(), 2),
                })
        df = pd.DataFrame(rows)
        print(f"  DataFrame: {df.shape[0]} жол × {df.shape[1]} баған")
        return df

    def groupby_grams(self):
        return (self.df.groupby("тағам")["граммы"]
                .sum().reset_index()
                .rename(columns={"граммы": "жалпы_граммы"})
                .sort_values("жалпы_граммы", ascending=False))

    def groupby_calories(self):
        return (self.df.groupby("тағам")["жалпы_ккал"]
                .sum().reset_index()
                .rename(columns={"жалпы_ккал": "жалпы_калория"})
                .assign(жалпы_калория=lambda x: x["жалпы_калория"].round(1))
                .sort_values("жалпы_калория", ascending=False))

    def groupby_full(self):
        return (self.df.groupby("тағам")
                .agg(
                    жалпы_граммы    =("граммы",      "sum"),
                    жалпы_ккал      =("жалпы_ккал",  "sum"),
                    ингредиент_саны =("ингредиент",  "count"),
                    орташа_ккал_100г=("ккал_100г",   "mean"),
                )
                .reset_index()
                .round(1)
                .sort_values("жалпы_ккал", ascending=False))

    def ingredient_frequency(self):
        return (self.df.groupby("ингредиент")["тағам"]
                .count().reset_index()
                .rename(columns={"тағам": "тағам_саны"})
                .sort_values("тағам_саны", ascending=False))

    def apply_calorie_label(self):
        def label(row):
            if row["жалпы_ккал"] < 50:
                return "аз"
            elif row["жалпы_ккал"] < 200:
                return "орта"
            else:
                return "жоғары"

        df2 = self.df.copy()
        df2["калория_деңгейі"] = df2.apply(label, axis=1)
        return df2[["тағам", "ингредиент", "жалпы_ккал", "калория_деңгейі"]]
    def save_csv(self, filename="талдау_нәтижесі.csv"):
        self.df.to_csv(filename, index=False, encoding="utf-8-sig")
        print(f"CSV сақталды: '{filename}'")

    def show_analysis(self):
        print("\n" + "─" * 52)
        print(" Тағам бойынша жалпы граммы:")
        print(self.groupby_grams().to_string(index=False))
        print(" Тағам бойынша жалпы калория:")
        print(self.groupby_calories().to_string(index=False))
        print(" Толық статистика (groupby + agg):")
        print(self.groupby_full().to_string(index=False))
        print(" Ингредиент жиілігі:")
        print(self.ingredient_frequency().to_string(index=False))
        print("  Калория деңгейі (apply):")
        print(self.apply_calorie_label().head(10).to_string(index=False))

class ChartBuilder:
    def __init__(self, pandas_analyzer):
        self.pa = pandas_analyzer
        sns.set_theme(style="whitegrid", palette="muted")

    def bar_grams(self, filename="диаграмма_граммы.png"):
        df = self.pa.groupby_grams()

        fig, ax = plt.subplots(figsize=(10, 5))
        colors = ["#e74c3c", "#3498db", "#2ecc71", "#f39c12", "#9b59b6"]
        bars = ax.barh(df["тағам"], df["жалпы_граммы"],
                       color=colors, edgecolor="white", height=0.6)

        for bar in bars:
            w = bar.get_width()
            ax.text(w + 10, bar.get_y() + bar.get_height() / 2,
                    f"{int(w)}г", va="center", fontsize=10)

        ax.set_title("Тағам бойынша жалпы ингредиент граммы",
                     fontsize=13, fontweight="bold", pad=12)
        ax.set_xlabel("Граммы")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        plt.tight_layout()
        plt.savefig(filename, dpi=150, bbox_inches="tight")
        plt.close()
        print(f"Сақталды: '{filename}'")

    def bar_calories(self, filename="диаграмма_калория.png"):
        df = self.pa.groupby_calories()

        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(df["тағам"], df["жалпы_калория"],
                      color=["#e67e22","#e74c3c","#c0392b","#d35400","#f39c12"],
                      edgecolor="white", width=0.5)

        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, h + 20,
                    f"{h:.0f}", ha="center", fontsize=10, fontweight="bold")

        ax.set_title("Тағам бойынша жалпы калория",
                     fontsize=13, fontweight="bold", pad=12)
        ax.set_xlabel("Тағам")
        ax.set_ylabel("Калория (ккал)")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        plt.tight_layout()
        plt.savefig(filename, dpi=150, bbox_inches="tight")
        plt.close()
        print(f" Сақталды: '{filename}'")

    def seaborn_heatmap(self, filename="диаграмма_жылу_картасы.png"):
        pivot = self.pa.df.pivot_table(
            index="тағам", columns="ингредиент",
            values="жалпы_ккал", aggfunc="sum", fill_value=0
        )

        fig, ax = plt.subplots(figsize=(14, 5))
        sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlOrRd",
                    linewidths=0.5, ax=ax, cbar_kws={"label": "ккал"})
        ax.set_title("Тағам × Ингредиент калория жылу картасы",
                     fontsize=13, fontweight="bold", pad=12)
        ax.set_xlabel("Ингредиент")
        ax.set_ylabel("Тағам")
        plt.xticks(rotation=40, ha="right", fontsize=8)
        plt.tight_layout()
        plt.savefig(filename, dpi=150, bbox_inches="tight")
        plt.close()
        print(f" Сақталды: '{filename}'")

    def seaborn_boxplot(self, filename="диаграмма_boxplot.png"):
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.boxplot(data=self.pa.df, x="тағам", y="граммы",
                    palette="pastel", ax=ax)
        ax.set_title("Ингредиент граммдарының таралуы (boxplot)",
                     fontsize=13, fontweight="bold", pad=12)
        ax.set_xlabel("Тағам")
        ax.set_ylabel("Граммы")
        plt.tight_layout()
        plt.savefig(filename, dpi=150, bbox_inches="tight")
        plt.close()
        print(f" Сақталды: '{filename}'")

    def build_all(self):
        print("\n  ▶ Диаграммалар жасалуда...")
        self.bar_grams("диаграмма_граммы.png")
        self.bar_calories("диаграмма_калория.png")
        self.seaborn_heatmap("диаграмма_жылу_картасы.png")
        self.seaborn_boxplot("диаграмма_boxplot.png")

if __name__ == "__main__":
    book = build_recipe_book()

    print("\n NumPy кеңейтілген операциялар:")
    np_adv = NumpyAdvanced(book)
    np_adv.show_matrix()
    np_adv.percentile_info()
    np_adv.where_example()

    print("\nPandas талдауы:")
    pa = PandasAnalyzer(book)
    pa.show_analysis()
    pa.save_csv("талдау_нәтижесі.csv")

    print("\nДиаграммалар:")
    charts = ChartBuilder(pa)
    charts.build_all()
