from aiohttp import web
import json
from PIL import Image
from io import BytesIO

from multidict import MultiDict
from db import db_insert, db_select


async def post_handler(request):
    if request.content_type != 'multipart/form-data':
        return web.Response(status=400, text='Используйте form/data для отправки изображения')
    for i in range(4):
        await request.content.readline()
    bytes_img = await request.content.read()
    p_img = Image.open(BytesIO(bytes_img))
    if p_img.format != 'JPEG':
        p_img = p_img.convert('RGB')
    output = BytesIO()
    p_img.save(output, format='JPEG')
    id_img = await db_insert(output.getvalue())
    data = {'image_id': id_img}
    return web.json_response(data, status=201)
    
async def get_handler(request):
    id = int(request.match_info['id'])
    db_bytes_img = await db_select(id)
    img = BytesIO(db_bytes_img)
    return web.Response(
        body=img.getvalue(), content_type="image/jpeg")