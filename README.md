## Реализация API чата на DJR

#### Установка:

1. >git clone https://bitbucket.org/soures1/isitestapp/src/master/
2. Создайте виртуальное окружение (virtualenv)
    >python3.7 -m venv env
3. Активируйте
    >source env/bin/activate
4. Установите зависимости:
    >pip install -r requirement.txt
5. Выполните миграцию БД:
    >./manage.py migrate
6. Создайте супер-пользователя:
    >./manage.py createsuperuser
7. Запустите тесты: 
    >./manage.py test
8. Запустите сервер:
    >./manage.py runserver

## API: