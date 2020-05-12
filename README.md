## Realization of API on DJR

#### Installation:

1. Clone repository

   
2. Create virtual environment (virtualenv)

    ```
    python3.7 -m venv env
    ```
3. Activate
    ```
    source env/bin/activate
    ```
4. Install dependency:
    ```
    pip install -r requirement.txt
    ```
5. Migrate DB:
    ```
    ./manage.py migrate
    ```
    ```
6. Create a super user:
    ```
    ./manage.py createsuperuser
    ```
7. Run tests:
    ```
    ./manage.py test
    ```
8. Run server:
    ```
    ./manage.py runserver
    ```

## API:

| URL       | Method                | Post Data (JSON) | Discription |
| --- |:---:| ---:| ---:|
| /api/v1/chat/create_chat/    | POST    | with_user : INT |  Create chat (Thread) with selected user |
| /api/v1/chat/delete_chat/<int:pk>/  | DELETE    | - |  Delete selected Thread by id|
| /api/v1/chat/chats/     | GET    | - | Get all chats of user with the last message |
| /api/v1/chat/messages/<ID>/     | GET    | - | Get all messages from selected chat by id |
| /api/v1/chat/messages/<ID>/     | POST    | message: String | Send message in selected chat by id |
| /api/v1/chat/read_messages/   | POST    | messages_list : List [int]  - The list of id messages| Sets the flag is_read to the selected messages |
| /api/v1/chat/get_unread_messages/   | GET    | - | Get the number of unread messages |





