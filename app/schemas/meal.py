from pydantic import BaseModel, Field
from typing import List, Optional

# Padrão de entrada (preenchida automaticamente com a soma dos ingredientes)
class MealRequest(BaseModel):
    ingredientes: List[str]
    calorias: Optional[float] = Field(None, gt=0)
    carboidratos: Optional[float] = Field(None, ge=0)
    proteinas: Optional[float] = Field(None, ge=0)
    gorduras: Optional[float] = Field(None, ge=0)

# gt=0 → maior que zero
# ge=0 → maior ou igual a zero