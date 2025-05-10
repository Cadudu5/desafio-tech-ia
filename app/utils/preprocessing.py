import pandas as pd


csv = 'food_data_complete.csv'

df = pd.read_csv(f"./data/raw/FOOD DATASET/{csv}")

df = df[['food', 'Caloric Value', 'Carbohydrates', 'Protein', 'Fat']]
print(df.head())

# Função de classificação com base nas heurísticas
## 
# 
# Nutriente	Novo limite sugerido	Justificativa
# Calorias	≤ 600–700 kcal	Refeições principais geralmente têm entre 400–700 kcal
# Carboidratos	≤ 60–75 g	Dependendo da porção e perfil da refeição
# Proteínas	≥ 15–20 g	Mantido proporcionalmente
# Gorduras	≤ 20–25 g	Considerando fontes boas (óleo, carnes magras)
# Classificação Final
# Saudável (1): alimento atende a pelo menos 3 dos 4 critérios
# Não saudável (0): atende a menos de 3 critérios
# ## 
def classificar_refeicao(row):
    criterios = 0
    if row['Caloric Value'] <= 700:
        criterios += 1
    if row['Carbohydrates'] <= 75:
        criterios += 1
    if row['Protein'] >= 15:
        criterios += 1
    if row['Fat'] <= 25:
        criterios += 1
    return 1 if criterios >= 3 else 0

df['classificacao'] = df.apply(classificar_refeicao, axis=1)

print('\n================================================\n')
print(df.head())
print(df['classificacao'].value_counts())
df.to_csv('./data/labels/food_labeled.csv') # Salvar o arquivo rotulado