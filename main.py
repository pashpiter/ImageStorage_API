from aiohttp import web

from settings import config
from logger_app import get_logger
from views import get_handler, get_logs, post_handler

routes = web.RouteTableDef()
app = web.Application()
logger = get_logger(__name__)

@routes.get('/{id}')
async def get(request):
    """Обработка GET-запросов"""
    return await get_handler(request)

@routes.get('/logs/{count}')
async def get_logs(request):
    """Обработка GET-запросов"""
    return await get_logs(request)

@routes.post('/')
async def post(request):
    """Обработка POST-запросов"""
    return await post_handler(request)


if __name__ == '__main__':
    app.add_routes(routes)
    app['config'] = config
    logger.warning('Start App')
    web.run_app(app)
