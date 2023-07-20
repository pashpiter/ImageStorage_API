from aiohttp import web

from authorization import check_token, create_token
from logger_app import get_logger
from views import get_handler, get_logs, post_handler


routes = web.RouteTableDef()
app = web.Application()
logger = get_logger(__name__)


@routes.get('/logs')
async def logs(request: web.Request) -> web.Response:
    """Обработка запроса на получения логов"""
    if not await check_token(request):
        return web.json_response({'error': 'Unauthorized'}, status=401)
    return await get_logs(request)


@routes.get('/{id}')
async def get(request: web.Request) -> web.Response:
    """Обработка GET-запросов c ID изображения"""
    if not await check_token(request):
        return web.json_response({'error': 'Unauthorized'}, status=401)
    return await get_handler(request)


@routes.post('/')
async def post(request: web.Request) -> web.Response:
    """Обработка POST-запросов"""
    if not await check_token(request):
        return web.json_response({'error': 'Unauthorized'}, status=401)
    return await post_handler(request)


@routes.post('/auth/token')
async def auth_get_token(request: web.Request) -> web.Response:
    _json_dict = await request.json()
    username, password = _json_dict.get('username'), _json_dict.get('password')
    if not username or not password:
        return web.Response(
            status=400,
            text='Для получения токена нужно ввести имя пользователя и пароль'
        )
    return await create_token(username, password, request.host + request.path)

if __name__ == '__main__':
    app.add_routes(routes)
    logger.warning('Start App')
    web.run_app(app)
