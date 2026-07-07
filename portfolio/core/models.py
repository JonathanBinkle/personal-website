from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os


class Files(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        blank=False,
        help_text="File name *with* extension.",
    )

    # upload files to settings.MEDIA_ROOT; OK to overwrite file with same name
    file = models.FileField(blank=True, storage=FileSystemStorage(allow_overwrite=True))

    class Meta:
        verbose_name_plural = "Files"

    def save(self, *args, **kwargs):
        old_name = self.file.name if self.pk else None

        # Clean name to prevent path traversal. Escape spaces.
        self.name = os.path.basename(self.name).replace(" ", "_")

        # Save file.
        self.file.save(self.name, self.file, save=False)
        super().save(*args, **kwargs)

        # Remove old file if self.name changed.
        if old_name and old_name != self.file.name:
            fs = FileSystemStorage(location=settings.MEDIA_ROOT)
            fs.delete(old_name)

    def __str__(self):
        return self.name
