from django.core.exceptions import PermissionDenied, ValidationError
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Item
from .serializers import ItemSerializer
from .authentication import JWTAuthentication

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
        user_id = self.request.user['payload']['id']
        item_id = request.data.get('item_id')

        try:
            item = Item.objects.get(id=item_id, user_id=user_id)
        except Item.DoesNotExist:
            raise PermissionDenied(f"Item with id {item_id} does not exist or belongs to another user.")

        if item.stock <= 0:
            raise PermissionDenied("Item is out of stock.")

        item.stock -= 1
        item.save()

        return Response({"message": "Item bought successfully."}, status=status.HTTP_200_OK)