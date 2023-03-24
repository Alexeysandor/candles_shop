# Первый pet проект
### Описание
Фронтенд часть написал самостоятельно с нуля, но особого внимания ей не уделяю, просто чтобы +- красиво было.
В бэкенде реализовано следующее:
  - Регистрация пользователя
  - Авторизация пользователя
  - Сброс пароля пользователя
  - Личный кабинет пользователя
  - Автозаполнение информации при оформлении заказа если профиль заполнен
  - Вывод из бд фотографий примеров товаров
  - Каталог товаров
  - Корзина товара
  - Просмотр информации о конкретном товаре
  - Оформление заказа
  - Просмотр информации о заказе
  
### Технологии
- Python 3.7
- Django 3.0
- Redis 4.3
- Docker
### Локальный запуск:
- Установите и активируйте виртуальное окружение
```
python -m venv venv
venv/scripts/activate
```
- Установите зависимости из файла requirements.txt
```
pip install -r requirements.txt
```

- В settings заменить данные бд на свои
- Выполнить миграции
```
python manage.py migrate
```
- При необходимости заполнить бд из дампа:
```
python manage.py loaddata db_dump.json
```
- В папке с файлом manage.py выполните команду:
```
python3 manage.py runserver
```
### Запуск в контейнерах:
- В директории infra создать .env файл и заполнить его данными, например:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
REDIS_HOST='redis://redis:6379/1'
```
- В директории infra выполнить команду:
```
docker-compose up -d --build
```
- Выполнить миграции командой:
```
docker-compose exec web python manage.py migrate
```
- Заполнить бд данными из дампа командой:
```
docker-compose exec web python manage.py loaddata db_dump.json
```
- В таком случае в бд уже будет суперпользователь с данными:
  - Логин: admin@gmail.com
  - Пароль: admin
- В противном случае создать суперпользователя командой:
```
sudo docker-compose exec web python manage.py createsuperuser
```
- Сервер будет доступен по адресу:
 - http://localhost/
- Спецификация API доступна по адресу:
 - http://localhost/redoc/
- Автор: Алексей Кузьменко
