# Nutri API 🍽️

API REST que classifica refeições como **saudáveis ou não saudáveis** com base em dados nutricionais. Desenvolvida com **Python 3.12**, **FastAPI** e **scikit-learn**.

---

### Como rodar o projeto localmente?

## 1 - Clone do repositório
git clone https://github.com/Cadudu5/desafio-tech-ia.git
cd desafio-tech-ia

## 2 - Contruir a imagem Docker
docker build -t nutri-api .

## 3 - Rodar o container
docker run -d -p 8000:8000 nutri-api

## 4 - A API ficará disponível em: http://localhost:8000/docs
Essa é a interface interativa onde você pode testar os endpoints.
Segue a baixo um exemplo de entrada correto ✅:
-{
    "ingredientes": [
        "peanuts cooked",
        "sausage mcgriddles mcdonalds"
    ]
}
- Os valores nutricionais são somados e calculados automaticamente, não precisa se preocupar com isso 😉

## 5 - Fique livre para testar diversas combinações de até 4 ingredientes, mas certifique-se de que o ingrediente está na lista.
- A lista de ingredientes está no arquivo:
    data/data_info/alimentos_catalogados.py
- Para gerar exemplos automaticamente, execute: 
    tests/generate_meals.py (fora do container)

## 🚀 Executando via Docker

### 1. Construir a imagem

bash
docker build -t nutri-api .

## Base de dados escolhida

A base de dados usada nesse projeto se chama 'Food Nutrition Dataset', e pode ser encontrada em
https://www.kaggle.com/datasets/utsavdey1410/food-nutrition-dataset para mais informações.

## 🧠 Raciocínio de Modelagem e Evolução

Inicialmente, o modelo foi treinado a partir de um dataset contendo valores nutricionais de alimentos isolados, rotulados por uma heurística simples baseada em 4 critérios:

- Calorias ≤ 700 kcal  
- Carboidratos ≤ 75 g  
- Proteínas ≥ 15 g  
- Gorduras ≤ 25 g  

Alimentos que atendiam a 3 ou mais critérios eram classificados como saudáveis (1), os demais como não saudáveis (0).

---

## 🔍 Problema identificado

Na API, os usuários fornecem refeições completas compostas por múltiplos ingredientes, e os valores nutricionais são somados. No entanto, o modelo original foi treinado apenas com itens unitários, o que levou a:

- Classificações incoerentes em algumas combinações de alimentos  
- Oscilações bruscas na probabilidade de predição  
- Penalizações excessivas quando apenas 1 critério era ultrapassado  

---

## ✅ Solução implementada

Para resolver isso, foi criado um novo dataset com refeições compostas realisticamente (de 2 a 4 ingredientes), geradas de forma aleatória a partir da base de alimentos.

Para cada refeição:

- Foram somados os valores nutricionais dos itens  
- A regra de ≥3 critérios atendidos foi reaplicada para gerar a nova label  
- O modelo foi re-treinado com esses novos dados  

---

## 📈 Resultado final

Após o re-treinamento com o novo dataset:

- O modelo passou a classificar corretamente refeições completas  
- A probabilidade retornada está mais estável e coerente com os nutrientes  
- Casos marginais (como a adição de 1 ingrediente leve) não causam mais inversões na classificação  
Esse ajuste permitiu que a API generalizasse bem para o caso real de uso, mantendo o raciocínio nutricional original implementado via aprendizado supervisionado.

## 🤖 Resultados estatísticos do treinamento do modelo

- Accuracy: 1.0
- Precision: 1.0
- Recall: 1.0
- F1-Score: 1.0

## 📊 Matriz de Confusão

|                      | Previsto: Não Saudável | Previsto: Saudável |
|----------------------|------------------------|---------------------|
| **Real: Não Saudável** | 759                    | 0                   |
| **Real: Saudável**     | 0                      | 1241                |

Esse dataset teve uma precisão máxima porque entendeu a nossa lógica de classificar alimentos como saudáveis ou não.
Essa regra foi muito simples, deixando o problema linearmente separável, o que foi tranquilo para o Random Forest.

