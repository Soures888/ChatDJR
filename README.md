## Реализация API чата на DJR

#### Установка:

* Клонируйте репозиторий
    ```
    git clone https://bitbucket.org/soures1/isitestapp/src/master/
    ```
* Создайте виртуальное окружение (virtualenv)
    ```
    python3.7 -m venv env
    ```
* Активируйте
    ```
    source env/bin/activate
    ```
* Установите зависимости:
    ```
    pip install -r requirement.txt
    ```
* Выполните миграцию БД:
    ```
    ./manage.py migrate
    ```
* Создайте супер-пользователя:
    ```
    ./manage.py createsuperuser
    ```
* Запустите тесты: 
    ```
    ./manage.py test
    ```
* Запустите сервер:
    ```
    ./manage.py runserver
    ```

## API:
