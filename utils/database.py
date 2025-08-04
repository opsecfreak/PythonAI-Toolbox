import os
from prisma import Prisma

db = Prisma()

async def connect_db():
    if not db.is_connected():
        await db.connect()

async def log_interaction(agent_name: str, prompt: str, response: str):
    try:
        await connect_db()
        await db.log.create(
            data={
                "agent_name": agent_name,
                "prompt": prompt,
                "response": response
            }
        )
    except Exception as e:
        print(f"Database error: {e}")
