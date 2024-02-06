from model import Food
import motor.motor_asyncio
import numpy as np

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://admin:admin@db-container:27017')
# Database Journal
database = client['Journal']
# Collection Food
collection = database.food


async def fetch_all_food():
    foods = []
    documents = collection.find({})
    async for document in documents:
        foods.append(Food(**document))
    return foods


async def calculate_total_macros_and_cals():
    sumMacros = np.zeros(3)
    documents = collection.find({})
    async for document in documents:
        sumMacros += np.array([document['carbs'], document['fat'], document['protein']]) * document['amount'] / 100
    sumCals = np.dot(np.array([4, 9, 4]), sumMacros)
    return {"sumMacros": sumMacros.tolist(), "sumCals": sumCals}


async def fetch_one_food(name):
    document = await collection.find_one({"name": name})
    return document


async def create_food(food):
    document = food
    result = await collection.insert_one(document)
    return document


async def remove_food(name):
    result = await collection.delete_one({"name": name})
    if result.deleted_count == 1:
        return True
    else:
        return False

