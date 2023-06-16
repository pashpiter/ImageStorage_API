import asyncpg

from logger_app import get_logger
from settings import config


logger = get_logger(__name__)


async def create_connection() -> asyncpg.Connection:
    """Настройка подключения к базе данных и создание таблицы"""
    database, user, password, host, port = config.values()
    try:
        conn = await asyncpg.connect(host=host, port=port, user=user,
                                     password=password, database=database)
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS images(
                id serial PRIMARY KEY,
                image BYTEA
            )
    ''')
    except Exception as e:
        logger.error(f'Connection to base with error:\n{e}')
    return conn


async def db_insert(bytes_image: bytes) -> int:
    """Добавление изображения в базу"""
    logger.info('Adding image to db')
    try:
        conn = await create_connection()
        await conn.execute('''
            INSERT INTO images(image) VALUES($1);
        ''', bytes_image)
        id_img = await conn.fetchval('''
            SELECT count(*) FROM images;
        ''')
        await conn.close()
    except Exception as e:
        logger.error(f'Adding to db ends with error:\n{e}')
    else:
        logger.info('Successful addition of the image to db')
    return id_img


async def db_select(id: int) -> bytes:
    """Получние изображения из базы по ID"""
    try:
        conn = await create_connection()
        img = await conn.fetchval('''
            SELECT image FROM images WHERE id=($1);
        ''', id)
        await conn.close()
    except Exception as e:
        logger.error(f'Getting image ends with error:\n{e}')
    return img
