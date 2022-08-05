# database.py


from dotenv import get_key
from motor.motor_asyncio import AsyncIOMotorClient


conn_str = f'mongodb+srv://{get_key(".env", "DB_LOGIN")}@nashbot.6c9wf.mongodb.net/?retryWrites=true&w=majority'
db_client = AsyncIOMotorClient(conn_str)
r_db = db_client.reminder_db
