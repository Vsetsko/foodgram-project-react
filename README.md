# Foodgram - продуктовый помощник.

## Описание проекта
На сайте пользователи могут публиковать кулинарные рецепты, подписываться 
на публикации рецептов других пользователей, добавлять понравившиеся рецепты в список 
«Избранное».

# Установка 

## Для локального запуска необходимо:

1. Клонируйте репозиторий на свой компьютер:

    ```bash
    git clone https://github.com/Vsetsko/foodgram-project-react.git
    ```
    ```bash
    cd foodgram-project-react
    ```
2. Создайте файл .env и заполните его своими данными. Перечень данных указан в корневой директории проекта в файле .env.example.

3. Собрать и запустить контейнеры:

    ```bash
    cd infra
    docker compose -f docker-compose_local.yml up -d
    ```

    После запуска контейнеров необходимо применить миграции, создать суперпользователя, собрать статику и загрузить базу ингридиентов:
    ```bash
    docker compose exec backend python manage.py migrate
    docker compose exec backend python manage.py createsuperuser
    docker compose exec backend python manage.py collectstatic --no-input
    docker compose exec backend python manage.py load_ingredients
    ```

## Деплой на сервере

1. Подключитесь к удаленному серверу:

    ```bash
    ssh -i путь_до_файла_с_SSH_ключом/название_файла_с_SSH_ключом имя_пользователя@ip_адрес_сервера 
    ```

2. Создайте на сервере директорию foodgram через терминал:

    ```bash
    mkdir foodgram
    cd foodgram
    ```

3. В директорию foodgram/ скопируйте или создайте файл .env:

    ```bash
    scp -i <path_to_SSH/SSH_name> .env <username@server_ip>:/home/<username>/foodgram/.env
    * ath_to_SSH — путь к файлу с SSH-ключом;
    * SSH_name — имя файла с SSH-ключом (без расширения);
    * username — ваше имя пользователя на сервере;
    * server_ip — IP вашего сервера.
    ```
    или
    ```bash
    sudo nano .env
    ```
4. Скопируйте файлы из локальной директории infra на сервер:

    ```text
    scp -r infra/* <username@server_ip>:/home/<username>/foodgram/
    ```
5. Запустите docker compose в режиме демона из папки infra:

    ```bash
    sudo docker compose -f docker-compose.yml up -d
    ```
