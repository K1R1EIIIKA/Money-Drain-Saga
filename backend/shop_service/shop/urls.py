from django.urls import path, include
from .views import ItemViewSet, BuyItemApiView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'items', ItemViewSet, basename='item')

urlpatterns = [
    path('', include(router.urls)),
    path('buy-item/', BuyItemApiView.as_view(), name='buy-item'),
]
