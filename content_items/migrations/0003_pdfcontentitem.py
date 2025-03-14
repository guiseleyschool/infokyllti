# Generated by Django 5.0.6 on 2024-05-22 07:22

import django.core.validators
import django.db.models.deletion
import infokyllti.storage_backends
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content_items', '0002_alter_imagelistitem_image_and_more'),
        ('tvdisplay', '0002_alter_contentitem_background_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='PdfContentItem',
            fields=[
                ('contentitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='tvdisplay.contentitem')),
                ('pdf_file', models.FileField(upload_to='pdfs', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])], verbose_name='PDF file')),
            ],
            options={
                'verbose_name': 'PDF file',
            },
            bases=('tvdisplay.contentitem',),
        ),
    ]
