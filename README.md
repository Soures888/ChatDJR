## Реализация API чата на DJR

#### Установка:

1. Клонируйте репозиторий
   
2. Создайте виртуальное окружение (virtualenv)
    ```
    python3.7 -m venv env
    ```
3. Активируйте
    ```
    source env/bin/activate
    ```
4. Установите зависимости:
    ```
    pip install -r requirement.txt
    ```
5. Выполните миграцию БД:
    ```
    ./manage.py migrate
    ```
6. Создайте супер-пользователя:
    ```
    ./manage.py createsuperuser
    ```
7. Запустите тесты: 
    ```
    ./manage.py test
    ```
8. Запустите сервер:
    ```
    ./manage.py runserver
    ```

## API:

| URL       | Метод                | Параметры | Описание |
| --- |:---:| ---:| ---:|
| /api/v1/chat/create_chat/    | POST    | with_user : INT |  Создаёт чат (Thread) с выбранным пользователем |
| /api/v1/chat/chats/     | GET    | - | Получает все чаты пользователя, с последним сообщением|
| /api/v1/chat/messages/<ID>/     | GET    | - | Получает все сообщения в выбранном чате по id |
| /api/v1/chat/messages/<ID>/     | POST    | message: String | Отправляет сообщение в выбранный чат по id |
| /api/v1/chat/read_message/<ID>/    | POST    | - | Ставит флаг is_read = True сообщению по ID|
| /api/v1/chat/get_unread_messages/   | GET    | - | Получает количество непрочитанных сообщений |





