import asyncpg

from settings import config
from logger_app import get_logger


logger = get_logger(__name__)

def create_connection() -> asyncpg.Connection:
    """Настройка подключения к базе данных"""
    return asyncpg.connect(config['postgres']['database_url'])

async def db_insert(bytes_image: bytes) -> int:
    """Добавление изображения в базу"""
    logger.info('Добавление изображения в базу')
    try:
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
    except Exception as e:
        logger.error(f'Добаление в базу закончилось с ошибкой:\n{e}')
    else:
        logger.info(f'Добавление изображения успешно завершено')
    return id_img

async def db_select(id: int) -> bytes:
    """Получние изображения из базы по ID"""
    try:
        conn = await create_connection()
        img = await conn.fetchval('''
            SELECT image FROM images WHERE id=($1);
        ''', id
        )
        await conn.close()
    except Exception as e:
        logger.error(f'Получение изображения закончилось с ошибкой:\n{e}')
    return img
