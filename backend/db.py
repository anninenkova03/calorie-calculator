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

async def calculate_calories():
    sumMacros = np.zeros(3)
    caloriesPerG = np.array([4,9,4])
    documents = collection.find({})
    async for document in documents:
        sumMacros += np.array([document['carbs'], document['fat'], document['protein']]) * document['amount'] / 100
    return np.dot(caloriesPerG, sumMacros)

async def fetch_one_food(name):
    document = await collection.find_one({"name": name})
    return document

async def create_food(food):
    nameInUse = await collection.find_one({"name": food['name']})
    sumMacros = food['carbs'] + food['fat'] + food['protein']
    if nameInUse or sumMacros != 100:
        return False
    else:
        document = food
        result = await collection.insert_one(document)
        return document

async def remove_food(name):
    result = await collection.delete_one({"name": name})
    if result.deleted_count == 1:
        return True
    return False
