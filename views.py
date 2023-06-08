from io import BytesIO

from aiohttp import web
from PIL import Image

from db import db_insert, db_select
from logger_app import get_logger

logger = get_logger(__name__)

async def get_handler(request: web.Request) -> web.Response:
    """Обрабатываем GET-запросы"""
    id = int(request.match_info['id'])
    logger.info(
        f'Получен GET-запрос с ID={id}',
        {'route': request.host+request.path}
    )
    db_bytes_img = await db_select(id)
    if not db_bytes_img:
        logger.error(
            f'Изображение с ID={id} в базе не найдено',
            {'route': request.host+request.path}
        )
        return web.Response(
            status=404, text=f'Изображение с ID={id} в базе не найден')
    bytes_img = BytesIO(db_bytes_img)
    return web.Response(
        body=bytes_img.getvalue(), content_type="image/jpeg")

async def post_handler(request: web.Request) -> web.json_response:
    """Обрабатываем POST-запросы"""
    logger.info('Получен POST-запрос', {'route': request.host+request.path})
    if request.content_type != 'multipart/form-data':
        logger.error(
            'Передан неподходящий контент',
            {'route': request.host+request.path}
        )
        return web.Response(
            status=400, text='Используйте form/data для отправки изображения')
    for i in range(4):
        await request.content.readline()
    bytes_img = await request.content.read()
    img, quality = Image.open(BytesIO(bytes_img)), 100
    if request.query.values():
        width = int(request.query.get('x', img.width))
        heigth = int(request.query.get('y', img.height))
        quality = int(request.query.get('quality', 100))
        if quality and not 0 < quality <= 100:
            return web.Response(
                status=400, text='Quality не может быть меньше 0 и больше 100')
        img = img.resize((width, heigth))
    if img.format != 'JPEG':
        img = img.convert('RGB')
    output = BytesIO()
    img.save(output, format='JPEG', quality=quality)
    id_img = await db_insert(output.getvalue())
    data = {'image_id': id_img}
    return web.json_response(data, status=201)

async def get_logs(request):
    """GET-запрос на получение логов"""
    count = int(request.match_info['count'])
    with open('logs.log', encoding='UTF-8') as f:
        log = [line for line in f]
    data = {f'last {count} logs': log[-count:]}
    return web.json_response(data)