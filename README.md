# ImageStorage_API


##### Стек: Python, aiohttp, Postgresql, asyncpg, Pillow
***

### Запуск проекта
Для запуска проекта необходимо: 
* Клонировать репозиторий
```
git clone https://github.com/pashpiter/ImageStorage_API
```
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
* Добавить в config.yaml параметры для Postgres
```
postgres:
  database_url: postgres://{user}:{password}@{ip_server}:{port}
```
* Запустить локальный сервер
```
python main.py
```

### Примеры команд API
* Загрузка изображения на сервер
```
POST http://{ip_server}:{port}/
```
* Загрузка изображения на сервер c дополнительными параметрами
```
POST http://{ip_server}:{port}/?x={int}&y={int}&quality={int}
```
* Получение изображения по ID
```
GET http://{ip_server}:{port}/{id}
```

#### Pavel Drovnin [@pashpiter](http://t.me/pashpiter)
