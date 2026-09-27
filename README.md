# SkyStore

Интернет-магазин цифровых продуктов на Django. В проекте подключена PostgreSQL, настроены модели каталога, админка, фикстуры и команда для загрузки тестовых данных.

## Возможности

- главная страница каталога и страница контактов
- модели `Category` и `Product`
- админ-панель для категорий и продуктов
- загрузка тестовых данных из фикстур

## Технологии

- Python 3.10
- Django 5.2
- PostgreSQL
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

5. Примените миграции, загрузите данные и запустите сервер:

```bash
python manage.py migrate
python manage.py fill_catalog
python manage.py runserver
```

Сайт будет доступен по адресу http://127.0.0.1:8000/

Админка: http://127.0.0.1:8000/admin/

## Полезные команды

```bash
python manage.py loaddata categories.json
python manage.py loaddata products.json
python manage.py fill_catalog
python manage.py shell
```

`fill_catalog` удаляет текущие категории и продукты, затем загружает данные из фикстур.

## Страницы

| Адрес | Описание |
| --- | --- |
| `/` | Главная страница каталога |
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
│   ├── models.py
│   └── views.py
├── config/
├── screenshots/
├── .env.example
├── manage.py
├── requirements.txt
└── README.md
```

## GitFlow

- `main` — стабильная версия
- `develop` — рабочая ветка разработки
- отдельные ветки для домашних заданий, pull request создаётся в `develop`
