# Используем образ Python 3.12 в качестве базового образа
FROM python:3.12.3

# Устанавливаем переменную окружения для запуска в неинтерактивном режиме
ENV PYTHONUNBUFFERED 1

# Создаем директорию для нашего кода и устанавливаем ее в качестве рабочей
RUN mkdir /app
WORKDIR /app

# Копируем файлы requirements.txt и устанавливаем зависимости
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта в рабочую директорию контейнера
COPY . /app/

# Определяем команду для запуска приложения с помощью runserver
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
