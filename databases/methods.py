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
            await tr.rollback()
        await conn.close()
        
    async def delete_expense(self,user_id,expense_number):
        conn = await asyncpg.connect(user='postgres',password='31591',host='localhost',database='usersandother')
        tr = conn.transaction()
        try:
            await tr.start()
            await conn.execute('DELETE FROM spends as s  USING numberedspends as n  WHERE s.user_id = $1 AND n.user_id = $1 AND n.number_of_expense = $2',user_id,expense_number)
            await tr.commit()
        except Exception as e:
            await tr.rollback()
        await conn.close()
        
    async def get_user_expenses(self,user_id):
        conn = await asyncpg.connect(user='postgres',password='31591',host='localhost',database='usersandother')
        data = await conn.fetch('SELECT amount,description,create_date,number_of_expense FROM numberedspends where user_id = $1',user_id)
        await conn.close()
        return [tuple(record) for record in data]
    
    async def delete_all_expenses(self,user_id):
        conn = await asyncpg.connect(user='postgres',password='31591',host='localhost',database='usersandother')
        tr = conn.transaction()
        try:
            await tr.start()
            await conn.execute('DELETE FROM spends   WHERE user_id = $1 ',user_id)
            await tr.commit()
        except Exception as e:
            print(f'failed:{e}')
            await tr.rollback()
        await conn.close()
