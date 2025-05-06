import asyncio
from database import db

async def insert_user():
    await db["users"].insert_one({
        "id": 1,
        "name": "Chồng yêu",
        "email": "chongyeu@example.com"
    })

asyncio.run(insert_user())