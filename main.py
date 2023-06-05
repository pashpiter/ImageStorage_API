from aiohttp import web
import os, sys
from PIL import Image
import json
from settings import config, BASE_DIR
from views import post_handler, get_handler


routes = web.RouteTableDef()
app = web.Application()

@routes.get('/{id}')
async def get(self):
    return await get_handler(self.request)

@routes.post('/')
async def post(self):
    return await post_handler(self.request)


if __name__ == '__main__':
    app.add_routes(routes)
    app['config'] = config
    web.run_app(app)