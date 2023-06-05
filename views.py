from aiohttp import web
import json
from PIL import Image
from io import BytesIO
from db import db_insert, db_select


async def post_handler(request):
    name = request.match_info.get('name', 'Anonymus')
    # if request.content_type == 'application/json':
    #     data = await request.json()
    #     text = json.dumps(data)
    #     return web.json_response(data, status=200)
    if request.content_type != 'multipart/form-data':
        return web.Response(status=400, text='Используйте form/data для отправки изображения')
    file = await request.multipart()
    field = await file.next()
    img = await request.content.read()
    # img_pillow = Image.frombytes('RGBA', (128,128), img)
    img_pillow = Image.open(BytesIO(img))
    db_img = await db_select(id=1)
    await db_insert(img)
    # if img_pillow.format != 'JPEG':
    #     jpg_img = img_pillow.convert('RGB')
    #     jpg_img.save('colors.jpg')
    # else:
    #     img_pillow.save('colors.jpg')
    
    # print(type(img_pillow))
    # print(type(img))
    return web.Response(text=str(db_img))
    
async def get_handler(request):
    id = request
    return