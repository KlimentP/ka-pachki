import pandas as pd

df = pd.read_csv("datasets/designs_from_niko.csv")
df["color_scheme"] = df[["Colors_1", "Colors_2", "Colors_3", "Colors_4", "Colors_5", "Colors_6"]].values.tolist()
df.color_scheme = df.color_scheme.apply(
    lambda x: list(set(k for k in x if pd.notnull(k)))
)

df.material = df.material.fillna("lid")
def quote_items(items):
    return '[' + ', '.join(f'"{item}"' for item in items) + ']'
df['color_scheme'] = df['color_scheme'].apply(quote_items)


df[["name", "material", "preferred_employee_id", "color_scheme"]].to_csv(
    "datasets/test2.csv", index=False
)
