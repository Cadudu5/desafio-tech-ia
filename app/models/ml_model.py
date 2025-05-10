import joblib
import numpy as np
from functools import lru_cache

class MealClassifier:
    def __init__(self):
        self.model = joblib.load("app/models/classifier.pkl")
        self.scaler = joblib.load("app/models/scaler.pkl")


    # Esse cache memoriza até 128 combinações únicas de ingredientes para montar uma refeição.
    @lru_cache(maxsize=128)
    def _cached_predict(self, calorias, carboidratos, proteinas, gorduras):
        features = np.array([[calorias, carboidratos, proteinas, gorduras]])
        scaled = self.scaler.transform(features)
        prob = self.model.predict_proba(scaled)[0][1]
        pred = int(prob >= 0.5)
        return pred, float(prob)

    def predict(self, calorias, carboidratos, proteinas, gorduras):
        return self._cached_predict(
            round(calorias, 2),
            round(carboidratos, 2),
            round(proteinas, 2),
            round(gorduras, 2)
        )

    def predict_from_ingredientes(self, ingredientes, df_base):
        ingredientes_normalizados = [i.strip().lower() for i in ingredientes]
        df_base["food_normalized"] = df_base["food"].str.strip().str.lower()
        df_refeicao = df_base[df_base["food_normalized"].isin(ingredientes_normalizados)]

        if df_refeicao.empty:
            raise ValueError("Nenhum ingrediente encontrado no banco de dados")

        calorias = df_refeicao["Caloric Value"].sum()
        carboidratos = df_refeicao["Carbohydrates"].sum()
        proteinas = df_refeicao["Protein"].sum()
        gorduras = df_refeicao["Fat"].sum()

        return self.predict(calorias, carboidratos, proteinas, gorduras)
