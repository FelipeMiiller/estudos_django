from datetime import datetime
import os
from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from shared.models import BaseModel


def files_upload_path(path, id, name, ext):
    name_slug = slugify(name)
    now = datetime.now()
    timestamp = now.strftime('%Y%m%d_%H%M%S_%f')
    return f'{path}/{id}/{name_slug}_{timestamp}{ext}'


class Category(BaseModel):
    class Meta:
        verbose_name = "categoria"
        verbose_name_plural = "categorias"

    name = models.CharField("Nome", max_length=100)
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        related_name='children',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


class Stock(BaseModel):
    class Meta:
        verbose_name = "estoque"
        verbose_name_plural = "estoque"

    product = models.OneToOneField(
        'Product',
        on_delete=models.PROTECT,
        related_name="stock",
        null=True,  # obrigatório!
        blank=True  # obrigatório!
    )
    quantity = models.IntegerField("Quantidade", default=0)
    min_quantity = models.IntegerField("Quantidade mínima", default=0)

    def __str__(self):
        return str(self.product.name)


class Brand(BaseModel):
    class Meta:
        verbose_name = "marca"
        verbose_name_plural = "marcas"

    name = models.CharField("Nome", max_length=100)

    def __str__(self):
        return str(self.name)


class Product(BaseModel):
    class Meta:
        verbose_name = "produto"
        verbose_name_plural = "produtos"

    name = models.CharField("Nome", max_length=100)
    description = RichTextField("Descrição", blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="prod_category", null=True, blank=True,verbose_name="Categoria")
    brand = models.ForeignKey(
        Brand, on_delete=models.PROTECT, related_name="prod_brand", null=True, blank=True,verbose_name="Marca")

    image_cover = models.ImageField(
        "Imagem principal", upload_to=lambda instance, filename: files_upload_path('products', instance.id, instance.name, os.path.splitext(filename)[1]))
    price = models.IntegerField("Preço", blank=True, null=True)
    price_decimal_places = models.IntegerField("Casas decimais", default=2)

    def get_price_decimal(self):
        if self.price is not None and self.price_decimal_places is not None:
            return self.price / (10 ** self.price_decimal_places)
        return None



class ProductImage(BaseModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='images')

    image = models.ImageField(
        "Imagem", upload_to=lambda instance, filename: files_upload_path('products', instance.product.id, instance.product.name, os.path.splitext(filename)[1]))

    class Meta:
        verbose_name = "imagem do produto"
        verbose_name_plural = "imagens do produto"

    def __str__(self):
        return f"Imagem do produto {self.product.name}"
