## Тестовое задание на позицию Fullstack разработчика (Python + React)

### Обновленная структура проекта
- Backend
```
backend/
├── migrations/             # Миграции базы данных (Alembic)
│   └── versions/           
└── src/                   
    ├── api/               
    │   └── v1/             # Эндпоинты (роутеры)
    ├── core/               # Конфигурация, настройки 
    ├── db/                 # Работа с базой данных
    │   ├── dao/            # DAO (Data Access Objects) 
    │   └── models.py       # Описание моделей 
    ├── schemas/            # Pydantic модели 
    ├── services/           # Слой бизнес-логики 
    ├── storage/           
    │   └── files/          # Локальное хранилище загруженных файлов
    └── tests/              # Тестовое покрытие
        ├── test_api/       # Unit-тесты роутеров (с моками сервисов)
        ├── test_dao/       # Интеграционные тесты базы данных 
        └── test_service/   # Тесты бизнес-логики 
```
- Frontend
```
frontend/
└── src/              
    ├── api/                    # Клиент для работы с Backend 
    ├── app/                    # Основная обертка App
    ├── components/             # UI-компоненты
    │   ├── AlertTable/         # Компонент отображения таблицы системных уведомлений
    │   ├── DashboardHeader/    # Шапка панели управления с основной информацией
    │   ├── FileTable/          # Таблица управления файлами (список, действия)
    │   ├── Pagination/         # Универсальный компонент навигации по страницам
    │   └── UploadModal/        # Модальное окно для загрузки новых файлов
    ├── hooks/                  # Кастомные React-хуки для бизнес-логики 
    ├── types/                  # Общие TypeScript интерфейсы и типы 
    └── utils/                  # Вспомогательные функции (форматтеры даты, размера файлов)
```

**Запуск:**
1. ```docker compose -f docker-compose.dev.yml up```
2. ```docker exec -it backend alembic upgrade head```

Локальный запуск (Unit-тесты)
3. ```pytest ```


**Открыть фронт:** ```http://localhost:3000/test``` 

**Открыть бэк:** ```http://localhost:8001/docs```