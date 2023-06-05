import asyncio
import asyncpg
from settings import config


def create_connection():
    return asyncpg.connect(config['postgres']['database_url'])

def db_create():
    conn = create_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXSIST images(
            id serial PRIMARY KEY,
            image BYTEA
        )
    ''')

async def db_insert(bytes_image):
    conn = await create_connection()
    await conn.execute('''
        INSERT INTO images(image) VALUES($1);
    ''', bytes_image
    )
    await conn.close()

async def db_select(id):
    conn = await create_connection()
    img = await conn.fetchval('''
        SELECT image FROM images WHERE id=($1);
    ''', id
    )
    await conn.close()
    return img
