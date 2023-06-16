# ImageStorage_API


##### Стек: Python, aiohttp, Postgresql, asyncpg, Pillow, Docker
***

### Запуск проекта
Для запуска проекта необходимо: 
* Клонировать репозиторий
```
git clone https://github.com/pashpiter/ImageStorage_API
```
* Перейти в папку ImageStorage_API
* Установить и активировать виртуальное окружение
```
python3 -m venv venv
```
```
source venv/bin/activate
```
* Установить зависимости из файла requirements.txt
```
pip install -r requirements.txt
```
* Добавить в корень папку config и созадть файл config.yaml
* Добавить в config.yaml параметры
```
POSTGRES_DB: postgres
POSTGRES_USER: {user}
POSTGRES_PASSWORD: {password}
POSTGRES_HOST: {ip_server}  # 0.0.0.0
POSTGRES_PORT: {port}  # 5432
```
* Запустить docker-compose для создания контейнера postgres
```
sudo docker-compose up -d
```
* Запустить локальный сервер
```
python main.py
```

### Примеры команд API
* Получение токена для пользователя
```
POST http://{ip_server}:{port}/auth/token
{
  "username": {str},
  "password": {str}
}
```
```
curl -X POST "http://0.0.0.0:8080/auth/token" \
-H "Content-Type: application/json" \
-d '{"username": "{username}", "password": "{password}"}'
```
* Загрузка изображения на сервер
```
POST http://{ip_server}:{port}/
```
```
curl -X POST "http://0.0.0.0:8080/" \
-H "Content-Type: multipart/form-data" \
-H "Authorization: Bearer {token}" \
-F "data=@{filename}"
```
* Загрузка изображения на сервер c дополнительными параметрами
```
POST http://{ip_server}:{port}/?x={int}&y={int}&quality={int}
```
```
curl -X POST "http://0.0.0.0:8080/?x={int}&y={int}&quality={int}" \
-H "Content-Type: multipart/form-data" \
-H "Authorization: Bearer {token}" \
-F "data=@{filename}"
```
* Получение изображения по ID
```
GET http://{ip_server}:{port}/{id}
```
```
curl "http://0.0.0.0:8080/{id}" \
-H "Authorization: Bearer {token}" \
-o image_from_response.jpeg
```
* Получение последних записей логов с необязательным параметром count
```
GET http://{ip_server}:{port}/logs?count={int}
```
```
curl "http://0.0.0.0:8080/logs?count={int}" \
-H "Authorization: Bearer {token}"
```

#### Pavel Drovnin [@pashpiter](http://t.me/pashpiter)
