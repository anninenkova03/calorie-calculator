from fastapi import FastAPI, HTTPException
from model import Food
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import httpx

from db import(
    fetch_all_food,
    fetch_one_food,
    create_food,
    remove_food,
    calculate_total_macros_and_cals
)
# App
app = FastAPI()

origins = ['https://localhost:8000', 'http://localhost:8000']

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_route():
    return {"Send": "Receive"}


@app.get("/api/food/all", name="trial")
async def get_food():
    async with httpx.AsyncClient() as client:
        response = await fetch_all_food()
    return response


@app.get("/api/food/{name}", response_model=Food)
async def get_food_by_name(name):
    async with httpx.AsyncClient() as client:
        response = await fetch_one_food(name)
    if response:
        return response
    raise HTTPException(404, f"Could not find a food with this name {name}")


@app.post("/api/food/add", response_model=Food)
async def post_food(food: Food):
    async with httpx.AsyncClient() as client:
        response = await create_food(food.dict())
    if response:
        return response
    raise HTTPException(400, f"Problem! Try again later")

@app.delete("/api/food/delete/{name}")
async def delete_food(name):
    async with httpx.AsyncClient() as client:
        response = await remove_food(name)
    if response:
        return response
    else:
        raise HTTPException(404, f"Could not find a food with this name: {name}")

@app.get("/api/food/calculate_total_macros_and_cals")
async def calculate_total_macros_and_cals():
    async with httpx.AsyncClient() as client:
        response = await calculate_total_macros_and_cals()
    return response
