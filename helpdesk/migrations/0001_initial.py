# Generated by Django 3.1.6 on 2021-02-20 19:34

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.crypto
import helpdesk.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default=django.utils.crypto.get_random_string, max_length=12, unique=True)),
                ('status', models.CharField(choices=[('Pending', 'En espera'), ('Ongoing', 'En curso'), ('Closed', 'Cerrado')], default='pending', max_length=20)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('department', models.CharField(choices=[('Frontline', 'Frontline'), ('Back-office', 'Back-office'), ('Workforce', 'Workforce'), ('IT', 'IT'), ('Management', 'Management')], max_length=20)),
                ('category', models.CharField(choices=[('Sala de Reuniones', 'Sala de Reuniones'), ('OT', 'OT'), ('VTO', 'VTO'), ('Vacations', 'Vacaciones'), ('Cita Médica', 'Cita Médica'), ('Cita Aseguradora', 'Cita Aseguradora')], max_length=20)),
                ('is_escalated', models.BooleanField(default=False, help_text='Marcarlo sólo si este issue ya fue atendido previamente.', verbose_name='es escalado')),
                ('subject', models.CharField(help_text='Escribe un título.', max_length=200)),
                ('description', models.TextField(help_text='Describe cuál es el problema.')),
                ('agent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assigned_tickets', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='Vacation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('from_date', models.DateField(default=datetime.date.today, verbose_name='from')),
                ('to_date', models.DateField(default=datetime.date.today, verbose_name='to')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('declined', 'Declined')], default='pending', max_length=20)),
                ('mensajito', models.CharField(default='¡Vacaciones! Bien merecidas', max_length=300)),
                ('agent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vacations_assigned', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vacations', to=settings.AUTH_USER_MODEL)),
                ('ticket', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='vacations', to='helpdesk.ticket')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('header', models.CharField(max_length=200)),
                ('body', models.TextField(blank=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logs', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('content', models.TextField(help_text='Escribe aquí tu mensaje.', verbose_name='content')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='helpdesk.ticket')),
            ],
        ),
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(blank=True, upload_to=helpdesk.models.attachments_upload_url)),
                ('description', models.CharField(help_text='Describe el propósito de la imagen.', max_length=200)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to=settings.AUTH_USER_MODEL)),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='helpdesk.ticket')),
            ],
        ),
    ]