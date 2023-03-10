# Generated by Django 4.1.5 on 2023-01-30 08:43

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helpdesk', '0004_alter_ticket_category_alter_ticket_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='code',
            field=models.CharField(default='L4DgoEednBDq', max_length=12, unique=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='description',
            field=ckeditor.fields.RichTextField(help_text='Uraian masalah'),
        ),
        migrations.AlterField(
            model_name='vacation',
            name='mensajito',
            field=models.CharField(default='Kami akan menanti Anda, {self.owner}. silakan offline :)', max_length=300),
        ),
    ]
