from django.db import models
from django.shortcuts import reverse
from django.utils.crypto import get_random_string
from django.conf import settings
from .mensajitos import MENSAJITOS_APPROVED
from ckeditor.fields import RichTextField
import random
import datetime as dt

def attachments_upload_url(self, *args, **kwargs):
    return f'attachments/{self.ticket.owner}/{self.ticket.code}/attach.png'

# TODO : Borrar este código y hacer migraciones.
# class Account(models.Model):
#     is_user = models.BooleanField(default=False)
#     is_agent = models.BooleanField(default=False)


class Ticket(models.Model):

    DEPARTMENT_CHOICES = (
        ('Kendari', 'Kejari Kendari'),
        ('Bombana', 'Kejari Bombana'),
        ('Kolaka', 'Kejari Kolaka'),
        ('Kolaka Utara', 'Kejari Kolaka Utara'),
        ('Muna', 'Kejari Muna'),
        ('Konsel', 'Kejari Konawe Selatan'),
        ('Konawe', 'Kejari Konawe'),
        ('Buton', 'Kejari Buton'),
        ('Wakatobi', 'Kejari Wakatobi'),
        ('Baubau', 'Kejari Baubau'),
    )

    CATEGORY_CHOICES = (
        ('Perencanaan', 'Perencanaan'),
        ('Penganggaran', 'Penganggaran'),
        ('Pengadaan', 'Pengadaan'),
        ('Pelaksanaan', 'Pelaksanaan Proyek'),
        ('Pengawasan', 'Pengawasan Kegiatan'),
        ('Serah Terima', 'Serah Terima Pekerjaan'),
        ('Purna Jual', 'Purna Juala'),
        ('Evaluasi Kegiatan', 'Evaluasi Kegiatan'),
    )

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Ongoing', 'On Going'),
        ('Closed', 'Closed'),
    )

    # Fields que el sistema va a llenar automáticamente.
    code = models.CharField(
        max_length=12, default=get_random_string(length=12), unique=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tickets', null=True, blank=True)
    agent = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assigned_tickets', blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="Pending")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # Fields que el usuario va a suministrar.
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES, blank=False)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, blank=False)
    is_escalated = models.BooleanField(
        verbose_name='eskalasi', default=False, help_text="Apakah akan dieskalasi?")
    subject = models.CharField(max_length=200, help_text="Subyek.")
    description = RichTextField(
        blank=False, help_text="Uraian masalah")

    # Ordena los Tickets de más reciente a más antiguo.
    # El .first() element del QuerySet es el ticket más reciente.
    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'code: {self.code} - date: {self.created}'

    def get_absolute_url(self):
        return reverse('helpdesk:ticket_detail', args=[self.created.year,
                                                       self.created.month,
                                                       self.created.day,
                                                       self.code])


class Comment(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, related_name='comments')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    content = RichTextField(
        verbose_name='content', blank=False, help_text="Escribe aquí tu mensaje.")

    def __str__(self):
        return f'from {self.owner} on ticket #{self.ticket.code}'


class Attachment(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='attachments')
    ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, related_name='attachments')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to=attachments_upload_url, blank=True)
    description = models.CharField(max_length=200,
        blank=False, help_text="Describe el propósito de la imagen.")


class Log(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='logs')
    date = models.DateTimeField(auto_now_add=True)
    header = models.CharField(max_length=200)
    body = models.TextField(blank=True)

    def __str__(self):
        return f'user: {self.user} - {self.date}'


class Vacation(models.Model):
    VACATION_STATUS = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
    )

    ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, related_name='vacations', blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vacations')
    agent = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vacations_assigned', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    from_date = models.DateField(verbose_name="from", default=dt.date.today)
    to_date = models.DateField(verbose_name="to", default=dt.date.today)
    status = models.CharField(max_length=20, choices=VACATION_STATUS, default='pending')
    mensajito = models.CharField(max_length=300, default=f''.join(random.choices(MENSAJITOS_APPROVED)))
    
    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'owner: {self.owner} - {self.status}'