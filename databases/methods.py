import asyncpg
import asyncio
class DatabaseHolder():
    async def add_user(self,user_id,username):
        conn = await asyncpg.connect(user='postgres',password='31591',host='localhost',database='usersandother')
        tr = conn.transaction()
        try:
            await tr.start()
            await conn.execute('INSERT INTO users(user_id,username) VALUES($1,$2)',user_id,username)
            await tr.commit()
        except:
            await tr.rollback()
        await conn.close()

    async def delete_user(self,user_id):
        conn = await asyncpg.connect(user='postgres',password='31591',host='localhost',database='usersandother')
        tr = conn.transaction()
        try:
            await tr.start()
            await conn.execute('DELETE FROM users WHERE user_id = $1',user_id)
            await tr.commit()
        except:
            await tr.rollback()
        await conn.close()
    async def add_expense(self,amount,user_id,currency,create_date,description):
        conn = await asyncpg.connect(user='postgres',password='31591',host='localhost',database='usersandother')
        tr = conn.transaction()
        try:
            await tr.start()
            await conn.execute('INSERT INTO spends(amount,user_id,currency,create_date,description) VALUES($1,$2,$3,$4,$5)',amount,user_id,currency,create_date,description)
            await tr.commit()
        except Exception as e:
            print(f'failed to connect:{e}')
            await tr.rollback()
        await conn.close()
    async def delete_expense(self):
        pass
