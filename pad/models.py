from django.db import models
import os


class Pad(models.Model):
    code = models.CharField(max_length=20, unique=True, db_index=True)
    text_content = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Pad [{self.code}]"

    class Meta:
        db_table = 'pad'


def upload_to(instance, filename):
    return f'uploads/{instance.pad.code}/{filename}'


class PadFile(models.Model):
    FILE_TYPE_CHOICES = [
        ('document', 'Document'),
        ('image', 'Image'),
        ('pdf', 'PDF'),
        ('other', 'Other'),
    ]

    pad = models.ForeignKey(Pad, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to=upload_to)
    original_name = models.CharField(max_length=255)
    file_size = models.BigIntegerField(default=0)
    file_type = models.CharField(max_length=20, choices=FILE_TYPE_CHOICES, default='other')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.original_name} ({self.pad.code})"

    def get_file_type(self):
        ext = os.path.splitext(self.original_name)[1].lower()
        if ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg']:
            return 'image'
        elif ext == '.pdf':
            return 'pdf'
        elif ext in ['.doc', '.docx', '.txt', '.rtf', '.odt']:
            return 'document'
        else:
            return 'other'

    def save(self, *args, **kwargs):
        if self.file:
            self.file_size = self.file.size
            self.file_type = self.get_file_type()
        super().save(*args, **kwargs)

    def get_size_display(self):
        size = self.file_size
        if size < 1024:
            return f"{size} B"
        elif size < 1024 * 1024:
            return f"{size / 1024:.1f} KB"
        else:
            return f"{size / (1024 * 1024):.1f} MB"

    class Meta:
        db_table = 'pad_file'
        ordering = ['-uploaded_at']
