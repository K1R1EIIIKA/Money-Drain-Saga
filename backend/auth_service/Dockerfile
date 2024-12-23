FROM python:3.13-slim
WORKDIR /backend/auth_service
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
ENV PYTHONUNBUFFERED=1
CMD ["sh", "-c", "python manage.py migrate && python create_superuser.py && python manage.py runserver_plus 0.0.0.0:8000"]
