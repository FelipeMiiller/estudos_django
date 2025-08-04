from django.db import models
from ckeditor.fields import RichTextField
from app.shared.utils.ulid_genarate_utils import generate_ulid


CREATED_AT_LABEL = "Criado em"
UPDATED_AT_LABEL = "Atualizado em"


class Brand(models.Model):

    class Meta:
        verbose_name = "marca"
        verbose_name_plural = "marcas"

    id = models.CharField(primary_key=True, max_length=26,
                          default=generate_ulid, editable=False)
    name = models.CharField("Nome", max_length=100)
    created_at = models.DateTimeField(CREATED_AT_LABEL, auto_now_add=True)
    updated_at = models.DateTimeField(UPDATED_AT_LABEL, auto_now=True)

    def __str__(self):
        return str(self.name)


class Stock(models.Model):

    class Meta:
        verbose_name = "estoque"
        verbose_name_plural = "estoque"

    id = models.CharField(primary_key=True, max_length=26,
                          default=generate_ulid, editable=False)
    product = models.OneToOneField(
        'Product',
        on_delete=models.PROTECT,
        related_name="stock",
        null=True,  # obrigatório!
        blank=True  # obrigatório!
    )
    quantity = models.IntegerField("Quantidade", default=0)
    min_quantity = models.IntegerField("Quantidade mínima", default=0)
    created_at = models.DateTimeField(CREATED_AT_LABEL, auto_now_add=True)
    updated_at = models.DateTimeField(UPDATED_AT_LABEL, auto_now=True)

    def __str__(self):
        return str(self.product.name)


class Product(models.Model):

    class Meta:
        verbose_name = "produto"
        verbose_name_plural = "produtos"

    id = models.CharField(primary_key=True, max_length=26,
                          default=generate_ulid, editable=False)
    name = models.CharField("Nome", max_length=100)
    description = RichTextField("Descrição", blank=True)
    price = models.IntegerField("Preço", blank=True, null=True)
    price_decimal_places = models.IntegerField("Casas decimais", default=2)
    brand = models.ForeignKey(
        Brand, on_delete=models.PROTECT, related_name="prod_brand", null=True, blank=True)
    photo = models.ImageField("Foto",upload_to="products/", blank=True, null=True)

    created_at = models.DateTimeField(CREATED_AT_LABEL, auto_now_add=True)
    updated_at = models.DateTimeField(UPDATED_AT_LABEL, auto_now=True)

    def get_price_decimal(self) -> float:
        return self.price / (10 ** self.price_decimal_places)

    def __str__(self):
        return str(self.name)
