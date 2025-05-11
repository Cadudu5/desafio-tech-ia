"""
Gera um novo dataset com refeições combinadas (com 2,3 ou 4 itens), calcula
os nutrientes totais   e aplica a regra de classificação por refeição.

Requisitos:
    - data/ingredientes.json          -> lista de nomes de alimentos
    - data/labels/food_labeled.csv    -> valores Nutricionais por item
Saída:
    - data/labels/refeicoes_combinadas_labeled.csv
"""

import json
import random
from pathlib import Path
import pandas as pd

# -------------------------------------------------------------------
# CONFIGURAÇÕES
# -------------------------------------------------------------------
QTD_REFEICOES   = 10000      # quantas combinações gerar
ITENS_MIN, ITENS_MAX = 2, 4   # intervalo de itens por refeição
ARQUIVO_ING      = Path("./data/data_info/alimentos_catalogados.json")
ARQUIVO_NUTRI    = Path("./data/labels/food_labeled.csv")
ARQUIVO_SAIDA    = Path("./data/labels/refeicoes_combinadas_labeled.csv")

# -------------------------------------------------------------------
# 1. Carrega lista de ingredientes
# -------------------------------------------------------------------
with ARQUIVO_ING.open(encoding="utf-8") as f:
    ingredientes = json.load(f)
    if isinstance(ingredientes, dict):         # caso haja chave "ingredientes"
        ingredientes = ingredientes["ingredientes"]

ingredientes = [i.strip().lower() for i in ingredientes]

# -------------------------------------------------------------------
# 2. Carrega valores nutricionais por item
# -------------------------------------------------------------------
df_nutri = pd.read_csv(ARQUIVO_NUTRI)
df_nutri["food_normalized"] = df_nutri["food"].str.strip().str.lower()

# Mantém apenas colunas necessárias
cols_keep = ["food_normalized", "Caloric Value",
             "Carbohydrates", "Protein", "Fat"]
df_nutri = df_nutri[cols_keep]

# -------------------------------------------------------------------
# 3. Função de regra (>=3 critérios → saudável)
# -------------------------------------------------------------------
def rotular_refeicao(cal, carb, prot, fat):
    criterios = sum([
        cal  <= 700,
        carb <= 75,
        prot >= 15,
        fat  <= 25
    ])
    return 1 if criterios >= 3 else 0

# -------------------------------------------------------------------
# 4. Gera refeições aleatórias e calcula rótulo
# -------------------------------------------------------------------
refeicoes = []
rng = random.Random(42)   # reprodutibilidade

for _ in range(QTD_REFEICOES):
    itens = rng.sample(ingredientes, rng.randint(ITENS_MIN, ITENS_MAX))

    df_sel = df_nutri[df_nutri["food_normalized"].isin(itens)]
    # garante que todos os itens existem no CSV
    if len(df_sel) != len(itens):
        continue

    cal  = df_sel["Caloric Value"].sum()
    carb = df_sel["Carbohydrates"].sum()
    prot = df_sel["Protein"].sum()
    fat  = df_sel["Fat"].sum()

    rotulo = rotular_refeicao(cal, carb, prot, fat)

    refeicoes.append({
        "ingredientes": ", ".join(itens),
        "Caloric Value":     cal,
        "Carbohydrates": carb,
        "Protein":    prot,
        "Fat":     fat,
        "label": rotulo
    })

# -------------------------------------------------------------------
# 5. Salva CSV final
# -------------------------------------------------------------------
df_out = pd.DataFrame(refeicoes)
ARQUIVO_SAIDA.parent.mkdir(parents=True, exist_ok=True)
df_out.to_csv(ARQUIVO_SAIDA, index=False)

print(f"✅  Dataset gerado com {len(df_out)} refeições → {ARQUIVO_SAIDA}")
print(df_out.head())
