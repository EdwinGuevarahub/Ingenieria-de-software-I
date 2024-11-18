FROM python:3.8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
CMD ["sh", "-c", "python check_db.py --service-name mysql --ip db --port 5432 && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]