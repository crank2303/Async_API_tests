# Проектная работа 5 спринта
Тестирование endpoint'ов FastAPI


# Технологии для тестов
- Код приложения на Python + FastAPI;
- Приложение запускается под управлением сервера ASGI(uvicorn);
- Функциональные тесты реализованы с помощью pytest;
- Хранилище данных: ElasticSearch;
- Кеширование данных: Redis Cluster;
- Redis и ElasticSearch запускаются через Docker.

# Как развернуть проект

Склонируйте репозиторий
```
git clone git@github.com:crank2303/Async_API_sprint_2.git
```

Перейдите в каталог с проектом
```
cd Async_API_sprint_2
```

Скопируйте файл настроек окружения проекта
```
cp .env.example .env
```

Перейдите в каталог с тестами
```
cd tests/functional
```

Скопируйте файл настроек окружения для тестов
```
cp .env.example .env
```

Запустите сборку контейнера
```
docker compose up -d --build
```
<br>
<hr>

# Запуск тестов
<ul>
  <li>Тесты запускаются локально</li>
  <li>Установить интерпретатор, виртуальное окружение</li>
  <li>Установить модули из файла Async_API_sprint_2/tests/functional/requirements.txt</li>
  <li>Запустить тесты из каталога Async_API_sprint_2/tests/functional/src/</li>
</ul>
