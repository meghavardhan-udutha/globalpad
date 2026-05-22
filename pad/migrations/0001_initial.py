from django.db import migrations, models
import django.db.models.deletion
import pad.models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Pad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(db_index=True, max_length=20, unique=True)),
                ('text_content', models.TextField(blank=True, default='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={'db_table': 'pad'},
        ),
        migrations.CreateModel(
            name='PadFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=pad.models.upload_to)),
                ('original_name', models.CharField(max_length=255)),
                ('file_size', models.BigIntegerField(default=0)),
                ('file_type', models.CharField(
                    choices=[('document', 'Document'), ('image', 'Image'), ('pdf', 'PDF'), ('other', 'Other')],
                    default='other', max_length=20)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('pad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='pad.pad')),
            ],
            options={'db_table': 'pad_file', 'ordering': ['-uploaded_at']},
        ),
    ]
