import asyncpg
import asyncio
class DatabaseHolder():
    async def add_user(user_id,username):
        conn = await asyncpg.connect(user='postgres',password='31591',host='localhost',database='usersandother')
        tr = conn.transaction()
        try:
            await tr.start()
            await conn.execute('INSERT INTO users(user_id,username) VALUES($1,$2)',user_id,username)
            await tr.commit()
        except:
            await tr.rollback()
            await conn.close()