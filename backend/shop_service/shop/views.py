from django.core.exceptions import PermissionDenied, ValidationError
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
import requests

from .models import Item
from .serializers import ItemSerializer
from .authentication import JWTAuthentication

GET_USER_URL = 'http://127.0.0.1:8001/user/'
CREATE_TRANSACTION_URL = 'http://127.0.0.1:8002/transactions/create/'
CHECK_VALID_TOKEN = 'http://127.0.0.1:8001/verify-token/'
SPEND_MONEY_URL = 'http://127.0.0.1:8001/money/spend'

def is_token_valid(token):
    response = requests.post(CHECK_VALID_TOKEN, data={"token": token})
    if response.status_code != 200:
        return False

    return True

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    authentication_classes = [JWTAuthentication]
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    def get_queryset(self):
        user = self.request.user['payload']['id']
        return self.queryset.filter(is_active=True, user_id=user)

    @action(detail=False, methods=['put'], url_path='bulk-update')
    def bulk_update(self, request, *args, **kwargs):
        user_id = self.request.user['payload']['id']
        data = request.data

        if not isinstance(data, list):
            raise ValidationError("Expected a list of objects.")

        updated_items = []
        for item_data in data:
            item_id = item_data.get("id")

            # Проверка существования предмета
            try:
                item = Item.objects.get(id=item_id, user_id=user_id)
            except Item.DoesNotExist:
                raise PermissionDenied(f"Item with id {item_id} does not exist or belongs to another user.")

            # Если stock < 0, удаляем предмет
            if item_data.get("stock", 0) < 0:
                item.delete()
                continue

            # Обновляем данные предмета
            serializer = self.get_serializer(item, data=item_data, partial=True)
            serializer.is_valid(raise_exception=True)
            updated_item = serializer.save()
            updated_items.append(updated_item)

        return Response({"updated_items": ItemSerializer(updated_items, many=True).data}, status=status.HTTP_200_OK)


class BuyItemApiView(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            raise PermissionDenied("Необходим токен аутентификации")

        token = token.split(" ")[1]
        if not is_token_valid(token):
            raise PermissionDenied("Токен недействителен")

        user_data = requests.get(GET_USER_URL, headers={"jwt": token}).json()
        if not user_data:
            raise PermissionDenied("Пользователь не найден")

        user_money = user_data.get("money")
        item_id = request.data.get("item_id")
        item = Item.objects.filter(id=item_id).first()
        if not item:
            raise PermissionDenied("Товар не найден")

        if user_money < item.price:
            raise PermissionDenied("Недостаточно средств")

        if requests.post(SPEND_MONEY_URL, headers={"jwt": token}, data={"money": item.price}).status_code != 200:
            raise PermissionDenied("Ошибка списания средств")

        item.save()

        return Response({"message": "Товар успешно куплен"}, status=status.HTTP_200_OK)