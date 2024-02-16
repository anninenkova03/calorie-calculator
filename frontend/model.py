from pydantic import BaseModel

class Food(BaseModel):
    name: str
    carbs: float
    fat: float
    protein: float
    amount: float
