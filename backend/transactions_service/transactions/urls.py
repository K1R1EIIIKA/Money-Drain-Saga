from django.urls import path

from transactions.views import TransactionListView, TransactionCreateView

urlpatterns = [
    path('transactions/', TransactionListView.as_view(), name='transaction-list'),
    path('transactions/create/', TransactionCreateView.as_view(), name='transaction-create'),
]