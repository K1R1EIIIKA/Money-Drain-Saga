import requests
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

AUTH_SERVICE_URL = "http://127.0.0.1:8001/verify-token/"  # Укажите путь к проверке токена


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            raise AuthenticationFailed("Необходим токен аутентификации")

        token = token.split(" ")[1]  # Извлекаем токен после "Bearer"

        try:
            response = requests.post(AUTH_SERVICE_URL, data={"token": token})
            if response.status_code != 200:
                raise AuthenticationFailed("Токен недействителен")
            user_data = response.json()  # Например: {"id": 1, "username": "test_user"}
            print(user_data)
        except requests.RequestException:
            raise AuthenticationFailed("Ошибка соединения с auth_service")

        return user_data, None
