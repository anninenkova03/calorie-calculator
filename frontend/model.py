from pydantic import BaseModel
import numpy as np

class FoodMacros(BaseModel):
    food: str
    macros: np.ndarray
    class Config:
        arbitrary_types_allowed=True


class Todo(BaseModel):
    title: str
    description: str
