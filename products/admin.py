import locale
from datetime import timedelta
from poplib import CR
from django.contrib import admin
from django.utils.html import strip_tags
from products.models import Brand, Category, Product, ProductImage, Stock
from django.utils.html import format_html

CREATE_AT_DISPLAY = 'Criado'
UPDATE_AT_DISPLAY = 'Atualizado'


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
    created_at_display.short_description = CREATE_AT_DISPLAY
    updated_at_display.short_description = UPDATE_AT_DISPLAY


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('full_path', 'parent',
                    'created_at_display', 'updated_at_display')
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at')

    def full_path(self, obj):
        names = []
        current = obj
        while current:
            names.append(current.name)
            current = current.parent
        return " > ".join(reversed(names))

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
    full_path.short_description = 'Caminho'
    name_display.short_description = 'Nome'
    created_at_display.short_description = CREATE_AT_DISPLAY
    updated_at_display.short_description = UPDATE_AT_DISPLAY


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    max_num = 5
    fields = ('image',)  # Adicione o campo de preview aqui
    show_change_link = True
    verbose_name_plural = 'Imagens'


class StockInline(admin.StackedInline):
    model = Stock
    can_delete = True  # permite deletar
    verbose_name_plural = 'Estoque'


class ProductAdmin(admin.ModelAdmin):

    # Add StockInline and ProductImageInline to ProductAdmin
    inlines = [StockInline, ProductImageInline]

    list_display = ('image_display', 'name_display', 'brand', 'description_display',
                    'stock_quantity_display', 'price_decimal_display', 'created_at_display', 'updated_at_display')
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at')

    class Media:
        # the django not provide the static files in the admin
        js = ('products/admin_image_preview.js',)

    def image_display(self, obj):
        if obj.image_cover:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius:50%;object-fit:cover;" />',
                obj.image_cover.url
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

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    # Alter the column names in the admin
    image_display.short_description = 'Imagem de capa'
    name_display.short_description = 'Nome'
    description_display.short_description = 'Descrição'
    stock_quantity_display.short_description = 'Estoque'
    price_decimal_display.short_description = 'Preço'
    created_at_display.short_description = CREATE_AT_DISPLAY
    updated_at_display.short_description = UPDATE_AT_DISPLAY


admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Product, ProductAdmin)
