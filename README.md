# Первый pet проект
### Описание
Фронтенд часть написал самостоятельно с нуля, но особого внимания ей пока не уделяю, просто чтобы красиво было.
В бэкенде реализовано следующее:
  Регистрация пользователя
  Авторизация пользователя
  Сессии для гостей
  Сброс пароля пользователя
  Личный кабинет пользователя
  Автозаполнение информации при оформлении заказа если профиль заполнен
  Вывод из бд фотографий примеров товаров
  Каталог товаров
  Корзина товара
  Просмотр информации о конкретном товаре
  Оформление заказа
  Удаление заказа
### Технологии
Python 3.7
Django 3.0
Redis 4.3
### Запуск проекта в dev режиме
- Установите и активируйте виртуальное окружение
```
python -m venv venv
venv/scripts/activate
```
- Установите зависимости из файла requirements.txt
```
pip install -r requirements.txt
```
- В папке с файлом manage.py выполните команду:
```
python3 manage.py runserver
```

Автор: Алексей Кузьменко