# SkyStore

Интернет-магазин цифровых продуктов на Django. В проекте подключена PostgreSQL, настроены модели каталога, админка, фикстуры и команда для загрузки тестовых данных.

## Возможности

- главная страница со списком товаров из базы
- регистрация и вход пользователей по email
- CRUD продуктов для авторизованных пользователей
- владелец продукта и модерация публикации
- кеширование Redis: страница продукта и список товаров категории
- валидация запрещённых слов и отрицательной цены в форме продукта
- форма обратной связи с сохранением сообщений в БД
- раздел статей: список опубликованных, просмотр со счётчиком, редактирование
- модели `User`, `Category`, `Product` и `Article`
- загрузка тестовых данных из фикстур

## Технологии

- Python 3.10
- Django 5.2
- PostgreSQL
- Redis
- Bootstrap 5
- Pillow
- IPython

## Установка и запуск

1. Клонируйте репозиторий и перейдите в папку проекта:

```bash
git clone https://github.com/largeorg-bit/django_lab.git
cd django_lab
```

2. Создайте базу данных PostgreSQL `skystore`.

3. Скопируйте шаблон переменных окружения и укажите свои данные:

```bash
copy .env.example .env
```

4. Создайте виртуальное окружение и установите зависимости:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

5. Запустите Redis на `127.0.0.1:6379` (Docker или локальный сервис):

```bash
docker run -d --name skystore-redis -p 6379:6379 redis:7-alpine
```

TTL кеша задаётся переменной `CACHE_TTL` (по умолчанию 60 секунд). Ключ списка товаров категории: `category_{id}`.

6. Примените миграции, загрузите данные и запустите сервер:

```bash
python manage.py migrate
python manage.py create_moderators
python manage.py fill_catalog
python manage.py runserver
```

Сайт будет доступен по адресу http://127.0.0.1:8000/

Админка: http://127.0.0.1:8000/admin/

## Полезные команды

```bash
python manage.py loaddata categories.json
python manage.py loaddata products.json
python manage.py loaddata articles.json
python manage.py create_moderators
python manage.py fill_catalog
python manage.py shell
```

`create_moderators` создаёт группу «Модератор продуктов» с правами `can_unpublish_product` и `delete_product`.

`fill_catalog` удаляет текущие категории и продукты, затем загружает данные из фикстур.

## Страницы

| Адрес | Описание |
| --- | --- |
| `/` | Главная страница каталога (доступна всем) |
| `/users/register/` | Регистрация |
| `/users/login/` | Вход |
| `/users/logout/` | Выход |
| `/categories/<id>/` | Товары выбранной категории (кеш Redis) |
| `/products/create/` | Создание продукта (только для авторизованных) |
| `/products/<id>/` | Карточка товара (кешируется, только для авторизованных) |
| `/products/<id>/edit/` | Редактирование (владелец или модератор) |
| `/products/<id>/delete/` | Удаление (владелец или модератор) |
| `/products/<id>/unpublish/` | Снятие с публикации (модератор) |
| `/articles/` | Список опубликованных статей |
| `/contacts/` | Контакты и форма обратной связи |
| `/admin/` | Админ-панель Django |

## Структура проекта

```text
django_lab/
├── catalog/
│   ├── fixtures/
│   ├── management/commands/
│   ├── migrations/
│   ├── templates/
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   └── views.py
├── blog/
│   ├── fixtures/
│   ├── templates/
│   ├── forms.py
│   ├── models.py
│   └── views.py
├── users/
│   ├── templates/
│   ├── forms.py
│   ├── models.py
│   └── views.py
├── config/
├── .env.example
├── manage.py
├── requirements.txt
└── README.md
```

## GitFlow

- `main` — стабильная версия
- `develop` — рабочая ветка разработки
- отдельные ветки для домашних заданий, pull request создаётся в `develop`
