# SkyStore

Интернет-магазин цифровых продуктов на Django. Проект развивается в рамках курса и на этом этапе содержит главную страницу каталога и страницу контактов.

## Возможности

- просмотр карточек товаров на главной странице
- страница контактов с формой обратной связи
- сообщение об успешной отправке формы

## Технологии

- Python 3.10
- Django 5.2
- Bootstrap 5

## Установка и запуск

1. Клонируйте репозиторий и перейдите в папку проекта:

```bash
git clone https://github.com/largeorg-bit/django_lab.git
cd django_lab
```

2. Создайте виртуальное окружение и установите зависимости:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

3. Примените миграции и запустите сервер:

```bash
python manage.py migrate
python manage.py runserver
```

Сайт будет доступен по адресу http://127.0.0.1:8000/

## Страницы

| Адрес | Описание |
| --- | --- |
| `/` | Главная страница каталога |
| `/contacts/` | Контакты и форма обратной связи |
| `/admin/` | Админ-панель Django |

## Структура проекта

```text
django_lab/
├── catalog/          # приложение каталога
│   ├── templates/
│   ├── urls.py
│   └── views.py
├── config/           # настройки Django-проекта
├── manage.py
├── requirements.txt
└── README.md
```

## GitFlow

- `main` — стабильная версия
- `develop` — рабочая ветка разработки
- отдельные ветки для домашних заданий, pull request создаётся в `develop`
