from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

def account_image_url(self, *args, **kwargs):
    return f'account_images/{self.owner}/profile.png'

def default_image_url():
    return f'account_images/account_default.png'

class MyUser(AbstractUser):
    """
    Según la documentación de Django, cada vez que empezamos un proyecto,
    lo mejor que podemos hacer es crear este modelo (incluso si el User por defecto 
    cumple con lo que necesitamos). Por si en un futuro queremos hacerle cambios.
    Más info: https://docs.djangoproject.com/en/3.1/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project
    """
    pass

class Account(models.Model):
    owner = models.OneToOneField(MyUser, verbose_name='account', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=account_image_url, default=default_image_url, blank=True)
    description = models.CharField(max_length=90, blank=True, 
                                    default="User Helpdesk Jaga Desa")
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    twitter = models.URLField(blank=True)

    def __str__(self):
        return f'{self.owner.username} account'.title()

    def social_links(self):
        links = {}
        if self.facebook != '':
            links['facebook'] = self.facebook
        if self.instagram != '':
            links['instagram'] = self.instagram
        if self.twitter != '':
            links['twitter'] = self.twitter

        return links
    

class Rol(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_regular = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)
    is_kejati = models.BooleanField(default=False)

    def get_user_role(self):
        if self.user.rol.is_regular:
            return 'Desa'
        elif self.user.rol.is_agent:
            return 'Kejari'
        elif self.user.rol.is_kejati:
            return 'Kejati'
        else:
            return f"Peran blm ditentukan"

    def __str__(self):
        if self.user.rol.is_regular:
            return f'{self.user} sebagai Desa'.title()
        elif self.user.rol.is_agent:
            return f'{self.user} sebagai Kejari'.title()
        elif self.user.rol.is_kejati:
            return f'{self.user} sebagai Kejati'.title()
        else:
            return f'{self.user}, Belum ditentukan'.title()