from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image
import re
import os


class Tags(models.Model):
    name = models.CharField(max_length=30, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Tags"

    def __str__(self):
        return self.name


class Images(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        blank=False,
        help_text="Image name *without* extension.",
    )

    # allow_overwrite=True to tell Django not to come up with alternative names
    image = models.ImageField(
        upload_to="blog_images/",
        blank=True,
        storage=FileSystemStorage(allow_overwrite=True),
        help_text=""" Currently, the maximum upload size is 10MB. Change
        'client_max_body_size <size>;' in nginx configuration if necessary. """,
    )

    class Meta:
        verbose_name_plural = "Images"

    def clean_img(self):
        """
        Strip potentially malicious non-image content from uploaded file.
        Returns the image format for convenience.
        """
        # Check if magic bytes indicate valid image
        try:
            img = Image.open(self.image)
        except Exception as e:
            raise ValidationError(f"Invalid image: {e}")

        if img.mode != "RGB":
            img = img.convert("RGB")

        # Strip non-image stuff by saving file in detected image format
        img_io = BytesIO()
        img_format = img.format.lower()
        img.save(img_io, format=img_format)
        img_content = ContentFile(img_io.getvalue(), self.image.name)

        # Save the cleaned image
        self.image.name = f"{self.name}.{img_format}".replace(" ", "_")
        self.image.save(self.image.name, img_content, save=False)

    def save(self, *args, **kwargs):
        old_name = self.image.name if self.pk else None

        # Clean name to prevent path traversal. Escape spaces.
        self.name = os.path.basename(self.name).replace(" ", "_")

        # Clean the image and save it
        self.clean_img()
        super().save(*args, **kwargs)

        # Remove old image if self.name changed
        if old_name and old_name != self.image.name:
            fs = FileSystemStorage(location=settings.MEDIA_ROOT)
            fs.delete(old_name)

    def __str__(self):
        return self.name


class Posts(models.Model):
    title = models.CharField(max_length=100, unique=True)
    teaser = models.CharField(max_length=500)
    content = models.TextField(null=True)
    datetime_published = models.DateTimeField(auto_now_add=True)
    datetime_last_modified = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(to=Tags, blank=True)
    reading_time = models.PositiveIntegerField(blank=True)  # compute on save()
    is_draft = models.BooleanField(default=False, blank=True, null=False)

    class Meta:
        ordering = ["-datetime_published"]
        verbose_name_plural = "Posts"

    def save(self, *args, **kwargs):
        # Compute estimate of reading time: get rough english word count and
        # assume that people can read about 238 WPM. Lower bound: 1 minute.
        self.reading_time = len(re.findall(r"\w+", self.content)) // 238 or 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
