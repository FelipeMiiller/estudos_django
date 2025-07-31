from uuid import uuid4
from django.db import models

# Create your models here.


class Product(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.IntegerField(blank=True, null=True)
    price_decimal_places = models.IntegerField(
        default=2)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def get_price_decimal(self) -> float:
        """Retorna o preço em formato decimal (ex: 12.34)."""
        return self.price / (10 ** self.price_decimal_places)
