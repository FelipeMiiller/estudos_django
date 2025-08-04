""" Admin of the Product model. """
import locale
from datetime import timedelta
from django.contrib import admin
from django.utils.html import strip_tags
from products.models import Brand, Product, Stock
from django.utils.html import format_html

class BrandAdmin(admin.ModelAdmin):


    list_display = ('name_display', 'created_at_display', 'updated_at_display')
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at')

    def name_display(self, obj):
        return obj.name

    def created_at_display(self, obj):
        if obj.created_at:
            return (obj.created_at - timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S')
        return "-"

    def updated_at_display(self, obj):
        if obj.updated_at:
            return (obj.updated_at - timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S')
        return "-"
    name_display.short_description = 'Nome'
    created_at_display.short_description = 'Criado em (UTC-3)'
    updated_at_display.short_description = 'Atualizado em (UTC-3)'


class StockInline(admin.StackedInline):
    model = Stock
    can_delete = False
    verbose_name_plural = 'Estoque'
    


class ProductAdmin(admin.ModelAdmin):

    inlines = [StockInline]  # Add the StockInline to the ProductAdmin
    list_display = ('image_display', 'name_display', 'brand', 'description_display', 'stock_quantity_display', 'price_decimal_display',
                    'price_decimal_places', 'created_at_display', 'updated_at_display')
    search_fields = ('name',)
    readonly_fields = ('photo_preview', 'created_at', 'updated_at')

    class Media:
        js = ('products/admin_photo_preview.js',) # the django not provide the static files in the admin

    def image_display(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius:50%;object-fit:cover;" />',
                obj.photo.url
            )
        return "-"
  

    def name_display(self, obj):
        return obj.name

    def description_display(self, obj):
        if obj.description:
            texto_limite = 50
            texto = strip_tags(str(obj.description))
            if len(texto) > texto_limite:
                return texto[:texto_limite] + "..."
            return texto
        return "-"

    def stock_quantity_display(self, obj):
        if obj.stock:
            return obj.stock.quantity
        return "-"

    def price_decimal_display(self, obj):
        if obj.price is not None and obj.price_decimal_places is not None:
            valor = obj.get_price_decimal()

            try:
                locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
                return locale.currency(valor, grouping=True)
            except locale.Error:
                return f'R$ {valor:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
        return "-"

    def created_at_display(self, obj):
        if obj.created_at:
            return (obj.created_at - timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S')
        return "-"

    def updated_at_display(self, obj):
        if obj.updated_at:
            return (obj.updated_at - timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S')
        return "-"
    
    
    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" width="100" height="100" style="border-radius:50%;object-fit:cover;" />',
                obj.photo.url
            )
        return "-"
    photo_preview.short_description = "Pré-visualização"

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    # Alter the column names in the admin
    image_display.short_description = 'Imagem'
    name_display.short_description = 'Nome'
    description_display.short_description = 'Descrição'
    stock_quantity_display.short_description = 'Estoque'
    price_decimal_display.short_description = 'Preço'
    created_at_display.short_description = 'Criado em (UTC-3)'
    updated_at_display.short_description = 'Atualizado em (UTC-3)'


admin.site.register(Brand, BrandAdmin)
admin.site.register(Product, ProductAdmin)
