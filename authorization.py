import io
from typing import Union

import jwt
import yaml
from aiohttp import web

from logger_app import get_logger
from settings import BASE_DIR


allowed_tokens_path = BASE_DIR / 'config' / 'allowed_tokens.yaml'
logger = get_logger(__name__)


async def add_or_return_token(
        username: str, token: str, password: str,
        f: io.TextIOWrapper, route: str, key: str
) -> web.Response:
    """Добавляет токен для пользователя в разрешенные или
    возвращает токен ддля пользователя созданный до этого"""
    parsed_tokens = yaml.safe_load(f)
    if (
        parsed_tokens and username not in parsed_tokens
    ) or not parsed_tokens:
        yaml.dump({username: token}, f)
        logger.info(f'Adding new token for {username}',
                    {'route': route})
        return web.json_response(data={'token': token}, status=201)
    if jwt.decode(
        parsed_tokens[username], key, algorithms="HS256"
    )['password'] != password:
        return web.json_response(
            data={'error': 'Неверный пароль'}, status=403)
    return web.json_response(data={'token': token}, status=200)


async def create_token(
        username: str, password: str, route: str
) -> web.Response:
    """Получение токена для пользователя"""
    logger.info(f'Get POST-request from {username} for getting token',
                {'route': route})
    key = 'secret'
    payload = {
        'username': username,
        'password': password
    }
    token = jwt.encode(payload, key)
    try:
        with open(allowed_tokens_path, 'r+') as f:
            return await add_or_return_token(username, token, password,
                                             f, route, key)
    except Exception:
        with open(allowed_tokens_path, 'w+') as f:
            return await add_or_return_token(username, token, password,
                                             f, route, key)


async def check_token(request: web.Request) -> Union[bool, web.Response]:
    """Проверка токена пользователя"""
    if not request.headers.get('Authorization'):
        return False
    logger.debug('Проверка токена', {'route': request.host + request.path})
    scheme, token = request.headers['Authorization'].strip().split(' ')
    if scheme != 'Bearer':
        return web.Response(status=400, text='Неподходящая схема токена')
    try:
        with open(allowed_tokens_path) as f:
            allowed_tokens = yaml.safe_load(f)
        return token in allowed_tokens.values() if allowed_tokens else False
    except FileNotFoundError:
        return False
