from django.contrib import admin

from .models import Item, ItemBundle, UserItem

admin.site.register(Item)
admin.site.register(ItemBundle)
admin.site.register(UserItem)
