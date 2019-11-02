from django.db import models
from uuid import uuid4
from django.contrib.auth.models import User


class Token(models.Model):
    token = models.UUIDField(verbose_name='token', default=uuid4)
    user = models.ForeignKey('auth.User', related_name='registration_tokens',
                             verbose_name='User', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.token)


class Team(models.Model):
    user_key = models.ForeignKey('auth.User', related_name='team', on_delete=models.PROTECT)
    project_key = models.ForeignKey('webapp.Project', related_name='team', on_delete=models.PROTECT)
    started_at = models.DateField(null=True, blank=True, verbose_name='Started at')
    ended_at = models.DateField(null=True, blank=True, verbose_name='Ended at')

    def __str__(self):
        return str(self.user_key)


class Profile(models.Model):
    avatar = models.ImageField(null=True, blank=True, upload_to='user_pics', verbose_name='Аватар')
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE, verbose_name='Пользователь')
    about_user = models.TextField(null=True, blank=True, verbose_name='О себе')
    git_profile = models.URLField(null=True, blank=True, verbose_name='Ссылка на Git профиль')

    def __str__(self):
        return self.user.get_full_name() + "'s Profile"

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

