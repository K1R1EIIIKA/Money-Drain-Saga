from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100, choices=[
        ('consumable', 'Consumable'),
        ('upgrade', 'Upgrade'),
        ('subscription', 'Subscription')
    ])

    def __str__(self):
        return self.name


class UserItem(models.Model):
    user_id = models.IntegerField()
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    @property
    def total_price(self):
        return self.item.price * self.quantity

    def __str__(self):
        return f'{self.item.name} - {self.quantity}'


class ItemBundle(models.Model):
    name = models.CharField(max_length=255)
    items = models.ManyToManyField(Item)
    discount = models.DecimalField(max_digits=4, decimal_places=2)

    @property
    def total_price(self):
        return sum(item.price for item in self.items.all()) * (1 - self.discount)

    def __str__(self):
        return f'{self.name} ({self.total_price})'
