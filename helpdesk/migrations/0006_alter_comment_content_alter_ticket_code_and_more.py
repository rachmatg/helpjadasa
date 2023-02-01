# Generated by Django 4.1.5 on 2023-01-30 08:43

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helpdesk', '0005_alter_ticket_code_alter_ticket_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=ckeditor.fields.RichTextField(help_text='Escribe aquí tu mensaje.', verbose_name='content'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='code',
            field=models.CharField(default='S7Tdq2L94f6U', max_length=12, unique=True),
        ),
        migrations.AlterField(
            model_name='vacation',
            name='mensajito',
            field=models.CharField(default='Kami kembali, {self.owner}! ;)', max_length=300),
        ),
    ]
