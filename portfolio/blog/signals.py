from blog.models import Images
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_delete
from django.core.files.storage import FileSystemStorage


@receiver(post_delete, sender=Images)
def delete_image(sender, instance, **kwargs):
    # Delete the underlying file on removal of model instance (not default).
    # Overwriting delete() doesn't work in case of multi-removal!
    if instance.image:
        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        fs.delete(instance.image.name)
