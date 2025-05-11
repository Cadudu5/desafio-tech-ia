import pandas as pd
import json

df = pd.read_csv(r'./data/labels/food_labeled.csv')

# Suponha que df seja o seu dataframe rotulado
alimentos_unicos = df["food"].dropna().unique().tolist()

# Criação do dicionário
dicionario_alimentos = {"alimentos": sorted(alimentos_unicos)}

# Salvar como arquivo JSON
with open(r"./data/data_info/alimentos_catalogados.json", "w", encoding="utf-8") as f:
    json.dump(dicionario_alimentos, f, ensure_ascii=False, indent=2)
