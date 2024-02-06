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
    cursor = collection.find({})
    async for document in cursor:
        # **document- any document
        foods.append(Food(**document))
    return foods


async def calculate_total_macros_and_cals():
    sumMacros = np.zeros(3)
    cursor = collection.find({})
    async for food in cursor:
        sumMacros += np.array([food['carbs'], food['fat'], food['protein']]) * food['amount'] / 100
    sumCals = np.dot(np.array([4, 9, 4]), sumMacros)
    return {'sumMacros': sumMacros.tolist(), 'sumCals': sumCals}


async def fetch_one_food(name):
    document = await collection.find_one({"name": name})
    return document


async def create_food(food):
    document = food
    # await dor the collection to insert the document
    result = await collection.insert_one(document)
    return document


async def remove_food(name):
    await collection.delete_one({"name": name})
    return True

