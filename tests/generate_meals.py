'''
 Esse Script pode ser usado para gerar novas combinações de refeições 
de acordo com os ingredientes em nossa base

'''


import json
import random
from pathlib import Path

def carregar_ingredientes(caminho_arquivo: str):
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data["ingredientes"] if isinstance(data, dict) else data

def gerar_refeicoes(ingredientes, qtd=5):
    refeicoes = []
    for _ in range(qtd):
        tamanho = random.randint(2, 4)
        refeicoes.append(random.sample(ingredientes, tamanho))
    return refeicoes

if __name__ == "__main__":
    ingredientes_path = Path("./data/data_info/alimentos_catalogados.json")
    ingredientes = carregar_ingredientes(ingredientes_path)
    refeicoes = gerar_refeicoes(ingredientes, qtd=10)

    for i, r in enumerate(refeicoes, 1):
        entrada_json = json.dumps({"ingredientes": r}, indent=2)
        print(f"Refeição {i}:\n{entrada_json}\n")
