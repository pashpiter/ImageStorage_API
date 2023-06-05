from aiohttp import web
import json
from PIL import Image
from io import BytesIO

from multidict import MultiDict
from db import db_insert, db_select


async def post_handler(request):
    name = request.match_info.get('name', 'Anonymus')
    # if request.content_type == 'application/json':
    #     data = await request.json()
    #     text = json.dumps(data)
    #     return web.json_response(data, status=200)
    if request.content_type != 'multipart/form-data':
        return web.Response(status=400, text='Используйте form/data для отправки изображения')
    for i in range(4):
        await request.content.readline()
    img = await request.content.read()
    p_img = Image.open(BytesIO(img))
    id_img = await db_insert(img)
    r = {'image_id': id_img}
    return web.json_response(r, status=201)
    
async def get_handler(request):
    id = int(request.match_info['id'])
    db_img = await db_select(id)
    img = Image.open(BytesIO(db_img))
    out = BytesIO(db_img)
    return web.Response(
        body=out, content_type="image/jpeg")