FROM python:3.13-slim
WORKDIR /backend/shop_service
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
ENV PYTHONUNBUFFERED=1
CMD ["python", "manage.py", "runserver_plus", "0.0.0.0:8000"]