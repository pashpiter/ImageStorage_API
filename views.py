from io import BytesIO

from aiohttp import web
from PIL import Image

from db import db_insert, db_select
from logger_app import get_logger


logger = get_logger(__name__)


async def get_handler(request: web.Request) -> tuple[web.Response,
                                                     web.json_response]:
    """Обрабатываем GET-запросы"""
    id = int(request.match_info['id'])
    logger.info(
        f'GET-request ID={id}',
        {'route': request.host + request.path}
    )
    if id < 1:
        return web.json_response(
            status=400,
            data={'error': 'ID должен быть больше 0'})
    db_bytes_img = await db_select(id)
    if not db_bytes_img:
        logger.error(
            f'No image with ID={id}',
            {'route': request.host + request.path}
        )
        return web.json_response(
            status=404,
            data={'error': f'Изображение с ID={id} в базе не найден'})
    bytes_img = BytesIO(db_bytes_img)
    return web.Response(
        body=bytes_img.getvalue(), content_type="image/jpeg")


async def post_handler(request: web.Request) -> web.json_response:
    """Обрабатываем POST-запросы"""
    logger.info('Get POST-request', {'route': request.host + request.path})
    if request.content_type != 'multipart/form-data':
        logger.error(
            'Incorrect content',
            {'route': request.host + request.path}
        )
        return web.json_response(
            status=400,
            data={'error': 'Используйте form/data для отправки изображения'})
    for i in range(4):
        await request.content.readline()
    bytes_img = await request.content.read()
    img, quality = Image.open(BytesIO(bytes_img)), 100
    if request.query.values():
        width = int(request.query.get('x', img.width))
        heigth = int(request.query.get('y', img.height))
        quality = int(request.query.get('quality', 100))
        if quality and not 0 < quality <= 100:
            return web.json_response(
                status=400,
                data={'error': 'Quality не может быть меньше 0 и больше 100'})
        img = img.resize((width, heigth))
    if img.format != 'JPEG':
        img = img.convert('RGB')
    output = BytesIO()
    img.save(output, format='JPEG', quality=quality)
    id_img = await db_insert(output.getvalue())
    return web.json_response(data={'image_id': id_img}, status=201)


async def get_logs(request: web.Request) -> web.json_response:
    """GET-запрос на получение логов"""
    count = int(request.query.get('count', 10))
    with open('logs.log', encoding='UTF-8') as f:
        log = [line for line in f]
    data = {f'last {count} logs': log[-count:]}
    return web.json_response(data)
