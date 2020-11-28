from datetime import date, datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


def custom_upload_to(instance, filename):
    # Eliminar imagen anterior
    # old_instance = Profile.objects.get(pk=instance.pk)
    # old_instance.avatar.delete()

    # Guardar fichero por fecha y hora en formato de directorios
    # return 'user_{}/avatar/{}/{}'.format(instance.user.id, datetime.today().strftime("%Y/%m/%d/%H/%M/%S/"), filename)

    return 'user_{}/avatar/{}/{}'.format(instance.user.id, date.today().strftime("%Y/%m/%d/"), filename)


class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=custom_upload_to, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    link = models.URLField(max_length=200, null=True, blank=True)

    class Meta:
        ordering = ['user__username']


@receiver(post_save, sender=User)
def ensure_profile_exists(sender, instance, **kwargs):
    if kwargs.get('created', False):
        Profile.objects.get_or_create(user=instance)
        # print("Se acaba de crear un usuario y su perfil enlazado")
