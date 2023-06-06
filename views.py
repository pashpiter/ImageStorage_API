from aiohttp import web
from PIL import Image
from io import BytesIO
from db import db_insert, db_select

    
async def get_handler(request: web.Request) -> web.Response:
    """Обрабатываем GET-запросы"""
    id = int(request.match_info['id'])
    db_bytes_img = await db_select(id)
    bytes_img = BytesIO(db_bytes_img)
    return web.Response(
        body=bytes_img.getvalue(), content_type="image/jpeg")

async def post_handler(request: web.Request) -> web.json_response:
    """Обрабатываем POST-запросы"""
    if request.content_type != 'multipart/form-data':
        return web.Response(
            status=400, text='Используйте form/data для отправки изображения')
    for i in range(4):
        await request.content.readline()
    bytes_img = await request.content.read()
    p_img = Image.open(BytesIO(bytes_img))
    if request.query.values():
        width = int(request.query.get('widht', p_img.width))
        heigth = int(request.query.get('height', p_img.height))
        quality = int(request.query.get('quality', 100))
        if quality and not 0 < quality <= 100: 
            return web.Response(
                status=400, text='Quality не может быть меньше 0 и больше 100')
        size = (p_img.width*quality//100, p_img.height*quality//100)
        resize_img = p_img.resize(
            (size)) if quality else p_img.resize((width, heigth))
    if resize_img.format != 'JPEG':
        resize_img = resize_img.convert('RGB')
    output = BytesIO()
    resize_img.save(output, format='JPEG')
    id_img = await db_insert(output.getvalue())
    data = {'image_id': id_img}
    return web.json_response(data, status=201)