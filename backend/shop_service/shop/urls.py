from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemViewSet, BuyItemApiView

router = DefaultRouter()
router.register(r'items', ItemViewSet, basename='item')
router.register(r'items/buy', BuyItemApiView, basename='item')

urlpatterns = [
    path('', include(router.urls)),
]
