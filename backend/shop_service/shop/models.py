from django.db import models

class Item(models.Model):
    user_id = models.IntegerField()
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100, choices=[
        ('consumable', 'Consumable'),
        ('upgrade', 'Upgrade'),
        ('subscription', 'Subscription')
    ])
    stock = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
