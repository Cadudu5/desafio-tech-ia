from fastapi import FastAPI
from app.schemas.meal import MealRequest
from app.models.ml_model import MealClassifier
import pandas as pd
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from fastapi import Request
from slowapi.errors import RateLimitExceeded
import logging

# Logging de requisições
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



app = FastAPI()
classifier = MealClassifier()

df_base = pd.read_csv(r"./data/labels/food_labeled.csv")
df_base["food_normalized"] = df_base["food"].str.strip().str.lower()
# Middleware de limite de requisição
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@limiter.limit("10/minute")
@app.post("/predict")
def predict_meal(data: MealRequest, request: Request):
    try:
        ingredientes_normalizados = [i.strip().lower() for i in data.ingredientes]
        df_refeicao = df_base[df_base["food_normalized"].isin(ingredientes_normalizados)]

        if df_refeicao.empty:
            return {"erro": "Nenhum dos ingredientes foi encontrado no banco de dados"}
        logger.info(f"Recebida requisição com ingredientes: {data.ingredientes}")

        # Preenche valores nutricionais automaticamente, se não enviados
        calorias = data.calorias if data.calorias is not None else df_refeicao["Caloric Value"].sum()
        carboidratos = data.carboidratos if data.carboidratos is not None else df_refeicao["Carbohydrates"].sum()
        proteinas = data.proteinas if data.proteinas is not None else df_refeicao["Protein"].sum()
        gorduras = data.gorduras if data.gorduras is not None else df_refeicao["Fat"].sum()

        pred, prob = classifier.predict(calorias, carboidratos, proteinas, gorduras)

        return {
            "classificacao": int(pred),
            "probabilidade": round(float(prob), 3),
            "mensagem": "Refeição classificada como saudável" if pred == 1 else "Refeição classificada como não saudável",
            "detalhes_nutricionais": {
                "calorias": float(calorias),
                "carboidratos": float(carboidratos),
                "proteinas": float(proteinas),
                "gorduras": float(gorduras)
            }
        }

    except Exception as e:
        return {"erro": f"Erro interno: {str(e)}"}
