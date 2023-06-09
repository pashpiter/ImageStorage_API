import jwt
import yaml
from aiohttp import web

from settings import BASE_DIR

allowed_tokens_path = BASE_DIR / 'config' / 'allowed_tokens.yaml'


async def create_token(username: str, password: str) -> web.json_response:
    """Получение токена для пользователя"""
    key = 'secret'
    payload = {
        'username': username,
        'password': password
    }
    token = jwt.encode(payload, key)
    with open(allowed_tokens_path, 'r+') as f:
        parsed_tokens = yaml.safe_load(f)
        if parsed_tokens and username not in parsed_tokens:
            yaml.dump({username: token}, f)
            data = {'token': token}
            return web.json_response(data, status=201)
        elif parsed_tokens and username in parsed_tokens:
            if jwt.decode(
                parsed_tokens[username], key, algorithms="HS256"
            )['password'] != password:
                return web.json_response(
                    data={'erorr': 'Неверный пароль'}, status=403)
        else:
            yaml.dump({username: token}, f)
        data = {'token': token}
    return web.json_response(data, status=201)


async def check_token(request: web.Request) -> bool:
    """Проверка токена пользователя"""
    if not request.headers.get('Authorization'):
        return False
    scheme, token = request.headers['Authorization'].strip().split(' ')
    if scheme != 'Bearer':
        return web.Response(status=400, text='Неподходящая схема токена')
    with open(allowed_tokens_path) as f:
        parsed_tokens = yaml.safe_load(f)
    return token in parsed_tokens.values()
