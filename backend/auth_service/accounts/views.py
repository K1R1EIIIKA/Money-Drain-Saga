from datetime import datetime, timedelta

import jwt
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView


class RegisterView(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        username = remove_invisible_characters(username)
        password = remove_invisible_characters(password)

        if User.objects.filter(username=username).exists():
            raise AuthenticationFailed('Пользователь уже существует')

        user = User(username=username)
        user.set_password(password)
        user.save()

        return Response({'message': 'Пользователь успешно зарегистрирован'})


def remove_invisible_characters(text):
    return ''.join(char for char in text if char.isprintable())


class VerifyTokenView(APIView):
    def post(self, request):
        token = request.data.get("token")
        if not token:
            raise AuthenticationFailed("Токен отсутствует")

        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Токен истёк")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Неверный токен")

        return Response({"payload": payload})



class LoginView(APIView):
    def post(self, request):
        print(jwt.__version__)
        username = request.data['username']
        password = request.data['password']

        username = remove_invisible_characters(username)
        password = remove_invisible_characters(password)

        print(1111111111111111)
        user = User.objects.filter(username=username).first()

        if user is None:
            raise AuthenticationFailed('Пользователь не найден')

        if not user.check_password(password):
            raise AuthenticationFailed('Неверный пароль')

        access_token_payload = {
            'id': user.id,
            'exp': datetime.utcnow() + timedelta(seconds=2600*24),
            'iat': datetime.utcnow()
        }

        refresh_token_payload = {
            'id': user.id,
            'exp': datetime.utcnow() + timedelta(seconds=3600 * 24),
            'iat': datetime.utcnow()
        }

        access_token = jwt.encode(access_token_payload, 'secret', algorithm='HS256')
        refresh_token = jwt.encode(refresh_token_payload, 'refresh_secret', algorithm='HS256')

        response = Response()
        response.set_cookie(key='jwt', value=access_token, httponly=True)
        response.set_cookie(key='refresh_jwt', value=refresh_token, httponly=True)
        response.data = {
            'jwt': access_token,
            'refresh_jwt': refresh_token
        }

        return response


class RefreshTokenView(APIView):
    def post(self, request):
        refresh_token = request.data['refresh_jwt']

        if not refresh_token or refresh_token == 'undefined':
            raise AuthenticationFailed('Не авторизован')

        try:
            payload = jwt.decode(refresh_token, 'refresh_secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Рефреш токен истек')

        access_token_payload = {
            'id': payload['id'],
            'exp': datetime.utcnow() + timedelta(seconds=3600),
            'iat': datetime.utcnow()
        }

        new_access_token = jwt.encode(access_token_payload, 'secret', algorithm='HS256')

        response = Response()
        response.set_cookie(key='jwt', value=new_access_token, httponly=True)
        response.data = {
            'jwt': new_access_token
        }

        return response


class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        print(token)

        if not token:
            raise AuthenticationFailed('Не авторизован')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Токен истек')

        user = User.objects.filter(id=payload['id']).first()
        print(user.username)
        response = Response()
        response.data = {
            'id': user.id,
            'username': user.username
        }

        return response



class LogoutView(APIView):
    def post(self, request):
        response = Response()

        if not request.COOKIES.get('jwt') or not request.COOKIES.get('refresh_jwt'):
            raise AuthenticationFailed('Не авторизован')

        response.delete_cookie('jwt')
        response.delete_cookie('refresh_jwt')

        response.data = {
            'message': 'Успешный выход'
        }

        return response