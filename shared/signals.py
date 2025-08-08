from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db.models import ImageField
import os
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

def convert_image_to_webp(fieldfile):
    """
    Converte o arquivo de imagem recebido para o formato WebP usando Pillow.
    Se já for WebP, retorna o arquivo original.
    Em caso de erro, retorna o arquivo original sem modificar.
    """
    if not fieldfile:
        return fieldfile
    try:
        img = Image.open(fieldfile)
        if img.format == 'WEBP':
            fieldfile.seek(0)
            return fieldfile
        buffer = BytesIO()
        img.save(buffer, format='WEBP', quality=90)
        return ContentFile(buffer.getvalue())
    except Exception:
        fieldfile.seek(0)
        return fieldfile

@receiver(pre_save)
def convert_all_imagefields_to_webp_and_delete_old(sender, instance, **kwargs):
    """
    Signal genérico para:
    - Converter qualquer ImageField para WebP antes de salvar (se não for webp)
    - Deletar o arquivo antigo do campo ImageField ao editar/trocar a imagem
    Aplica-se a todos os models do projeto automaticamente.
    """
    # Evita rodar para modelos internos do Django (ex: admin, auth, etc)
    if not hasattr(instance, '_meta') or instance._meta.app_label.startswith('django'):
        return

    # Busca a instância antiga, se existir (edição)
    if not instance.pk:
        old_instance = None  # Novo objeto, não existe anterior
    else:
        try:
            old_instance = sender.objects.get(pk=instance.pk)
        except sender.DoesNotExist:
            old_instance = None

    # Itera por todos os campos do tipo ImageField do model
    for field in instance._meta.get_fields():
        if isinstance(field, ImageField):
            image_file = getattr(instance, field.name)

            # --- Conversão automática para webp ---
            # Só converte se não for webp
            if image_file and hasattr(image_file, 'file') and image_file.name and not image_file.name.lower().endswith('.webp'):
                webp_file = convert_image_to_webp(image_file.file)
                image_file.save(os.path.splitext(image_file.name)[0]+'.webp', webp_file, save=False)

            # --- Deleção do arquivo antigo se mudou (edição) ---
            if old_instance:
                old_file = getattr(old_instance, field.name)
                # Só deleta se o arquivo antigo for diferente do novo
                if old_file and old_file != image_file:
                    old_file.delete(save=False)
