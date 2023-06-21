# ImageStorage_API


##### Стек: Python, aiohttp, Postgresql, asyncpg, Pillow, Docker
***

### Запуск проекта
_Есть вторая ветка deploy с запуском проекта через docker-compose_

Для запуска проекта в ветке main необходимо: 
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
POSTGRES_PORT: 5432
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
POST http://localhost:8080/auth/token
{
  "username": {str},
  "password": {str}
}
```
```
curl -X POST "http://localhost:8080/auth/token" \
-H "Content-Type: application/json" \
-d '{"username": "{str}", "password": "{str}"}'
```
* Загрузка изображения на сервер
```
POST http://localhost:8080/
```
```
curl -X POST "http://localhost:8080/" \
-H "Content-Type: multipart/form-data" \
-H "Authorization: Bearer {token}" \
-F "data=@{filename}"
```
* Загрузка изображения на сервер c дополнительными параметрами
```
POST http://localhost:8080/?x={int}&y={int}&quality={int}
```
```
curl -X POST "http://localhost:8080/?x={int}&y={int}&quality={int}" \
-H "Content-Type: multipart/form-data" \
-H "Authorization: Bearer {token}" \
-F "data=@{filename}"
```
* Получение изображения по ID
```
GET http://localhost:8080/{id}
```
```
curl "http://localhost:8080/{id}" \
-H "Authorization: Bearer {token}" \
-o image_from_response.jpeg
```
* Получение последних записей логов с необязательным параметром count
```
GET http://localhost:8080/logs?count={int}
```
```
curl "http://localhost:8080/logs?count={int}" \
-H "Authorization: Bearer {token}"
```

#### Pavel Drovnin [@pashpiter](http://t.me/pashpiter)
