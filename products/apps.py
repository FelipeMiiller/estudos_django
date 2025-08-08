from django.apps import AppConfig


class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'
    verbose_name = 'Produtos' # name visible in admin
    verbose_name_plural = 'Produtos' # name visible in admin

    def ready(self):
        import shared.signals  # Garante conexão dos signals globais
