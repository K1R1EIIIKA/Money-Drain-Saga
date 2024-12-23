from rest_framework import serializers
from .models import Item, ItemBundle


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class ItemBundleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemBundle
        fields = '__all__'
