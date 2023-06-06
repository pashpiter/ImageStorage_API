import asyncpg
from settings import config


def create_connection() -> asyncpg.Connection:
    """Настройка подключения к базе данных"""
    return asyncpg.connect(config['postgres']['database_url'])

def db_create() -> None:
    """Создание базы"""
    conn = create_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXSIST images(
            id serial PRIMARY KEY,
            image BYTEA
        )
    ''')

async def db_insert(bytes_image: bytes) -> int:
    """Добавление изображения в базу"""
    conn = await create_connection()
    await conn.execute('''
        INSERT INTO images(image) VALUES($1);
    ''', bytes_image
    )
    id_img = await conn.fetchval('''
        SELECT count(*) FROM images;
    '''
    )
    await conn.close()
    return id_img


async def db_select(id: int) -> bytes:
    """Получние изображения из базы по ID"""
    conn = await create_connection()
    img = await conn.fetchval('''
        SELECT image FROM images WHERE id=($1);
    ''', id
    )
    await conn.close()
    return img
