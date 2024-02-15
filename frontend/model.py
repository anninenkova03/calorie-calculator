from pydantic import BaseModel
import numpy as np

class Food(BaseModel):
    name: str
    carbs: float
    fat: float
    protein: float
    amount: float

    def getMacros(self):
        return np.array([self.carbs, self.fat, self.protein]) * [self.amount]
