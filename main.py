from aiohttp import web
from settings import config, BASE_DIR
from views import post_handler, get_handler


routes = web.RouteTableDef()
app = web.Application()

@routes.get('/{id}')
async def get(request):
    """Обработка GET-запросов"""
    return await get_handler(request)

@routes.post('/')
async def post(request):
    """Обработка POST-запросов"""
    return await post_handler(request)


if __name__ == '__main__':
    app.add_routes(routes)
    app['config'] = config
    web.run_app(app)