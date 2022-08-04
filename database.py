# database.py


from motor.motor_asyncio import AsyncIOMotorClient

conn_str = 'mongodb+srv://nashkw:oCN49lf0JjyD1Jgw@nashbot.6c9wf.mongodb.net/?retryWrites=true&w=majority'
db_client = AsyncIOMotorClient(conn_str)
r_db = db_client.reminder_db
