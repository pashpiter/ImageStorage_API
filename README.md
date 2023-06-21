# ImageStorage_API


##### Стек: Python, aiohttp, Postgresql, asyncpg, Pillow, Docker, nginx
***

### Запуск проекта
Для запуска проекта необходимо: 
* Клонировать репозиторий
```
git clone https://github.com/pashpiter/ImageStorage_API
```
* Перейти в папку ImageStorage_API

* Добавить в корень папку config и создать файл config.yaml
* Добавить в config.yaml параметры
```
POSTGRES_DB: postgres
POSTGRES_USER: {user}
POSTGRES_PASSWORD: {password}
POSTGRES_HOST: postgres
POSTGRES_PORT: 5432
```
* Запустить проект используя docker-compose
```
sudo docker-compose up -d
```

### Примеры команд API
* Получение токена для пользователя
```
POST http://localhost/auth/token
{
  "username": {str},
  "password": {str}
}
```
```
curl -X POST "http://localhost/auth/token" \
-H "Content-Type: application/json" \
-d '{"username": "{username}", "password": "{password}"}'
```
* Загрузка изображения на сервер
```
POST http://localhost/
```
```
curl -X POST "http://localhost/" \
-H "Content-Type: multipart/form-data" \
-H "Authorization: Bearer {token}" \
-F "data=@{filename}"
```
* Загрузка изображения на сервер c дополнительными параметрами
```
POST http://localhost/?x={int}&y={int}&quality={int}
```
```
curl -X POST "http://localhost/?x={int}&y={int}&quality={int}" \
-H "Content-Type: multipart/form-data" \
-H "Authorization: Bearer {token}" \
-F "data=@{filename}"
```
* Получение изображения по ID
```
GET http://localhost/{id}
```
```
curl "http://localhost/{id}" \
-H "Authorization: Bearer {token}" \
-o image_from_response.jpeg
```
* Получение последних записей логов с необязательным параметром count
```
GET http://localhost/logs?count={int}
```
```
curl "http://localhost/logs?count={int}" \
-H "Authorization: Bearer {token}"
```

#### Pavel Drovnin [@pashpiter](http://t.me/pashpiter)
