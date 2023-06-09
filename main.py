from aiohttp import web

from authorization import check_token, get_token
from logger_app import get_logger
from settings import config
from views import get_handler, get_logs, post_handler


routes = web.RouteTableDef()
app = web.Application()
logger = get_logger(__name__)


@routes.get('/{id}')
async def get(request):
    """Обработка GET-запросов"""
    if not check_token(request):
        return web.json_response({'erorr': 'Unauthorized'}, status=401)
    return await get_handler(request)


@routes.get('/logs/{count}')
async def logs(request):
    """Обработка запроса на получения логов"""
    if not check_token(request):
        return web.json_response({'erorr': 'Unauthorized'}, status=401)
    return await get_logs(request)


@routes.post('/')
async def post(request):
    """Обработка POST-запросов"""
    if not check_token(request):
        return web.json_response({'erorr': 'Unauthorized'}, status=401)
    return await post_handler(request)


@routes.post('/auth/token')
async def auth_get_token(request):
    json_dict = await request.json()
    username, password = json_dict.get('username'), json_dict.get('password')
    if not username or not password:
        return web.Response(
            status=400,
            text='Для получения токена нужно ввести имя пользователя и пароль'
        )
    return get_token(username, password)

if __name__ == '__main__':
    app.add_routes(routes)
    app['config'] = config
    logger.warning('Start App')
    web.run_app(app)
