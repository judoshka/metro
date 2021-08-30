# установка базового образа (host OS)
FROM python:3.8-slim
# установка рабочей директории в контейнере
WORKDIR /app
# копирование файла зависимостей в рабочую директорию
COPY . /app
# установка зависимостей
RUN pip install --no-cache-dir -r requirements.txt
# команда, выполняемая при запуске контейнера
CMD [ "python", "app.py" ]