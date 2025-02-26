FROM python:3.11.9-slim

WORKDIR /usr/src/date_me

#Устанавливаем netcat зависимость для выполнения entrypoint.sh скрипта(Миграции и фикстуры после запуска и готовности db-открытость порта db)
RUN apt-get update && apt-get install -y netcat-openbsd


ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .


#Убираем знак переноса каретки,который может появляться если файл создавался на виндовс
RUN sed -i 's/\r$//g' /usr/src/date_me/entrypoint.sh
#Даем права доступа на запуск на выполнение файлу entrypoint.sh
RUN chmod +x /usr/src/date_me/entrypoint.sh

ENTRYPOINT [ "./entrypoint.sh" ]