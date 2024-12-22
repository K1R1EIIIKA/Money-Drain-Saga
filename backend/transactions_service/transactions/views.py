from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Transaction


class TransactionListView(APIView):
    def get(self, request):
        transactions = Transaction.objects.all().values()
        return Response(transactions)


class TransactionCreateView(APIView):
    def post(self, request):
        data = request.data
        transaction = Transaction.objects.create(**data)
        return Response({'id': transaction.id}, status=status.HTTP_201_CREATED)
