from model import Food
import motor.motor_asyncio

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


async def fetch_one_food(name):
    document = await collection.find_one({"name": name})
    return document


async def create_food(food):
    document = food
    # await dor the collection to insert the document
    result = await collection.insert_one(document)
    return document


async def update_food(food):
    name = food['name']
    carbs = food['carbs']
    fat = food['fat']
    protein = food['protein']
    amount = food['amount']
    await collection.update_one({"name": name}, {"$set": {"carbs": carbs, "fat": fat, "protein": protein}})
    document = await collection.find_one({"name": name})

    return document


async def remove_food(name):
    await collection.delete_one({"name": name})
    return True

