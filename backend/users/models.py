from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.db.models import (CASCADE, CharField, EmailField, F, ForeignKey,
                              Model, Q, UniqueConstraint)


class User(AbstractUser):
    """ Модель пользователя. """

    first_name = CharField(
        'Имя',
        max_length=settings.LENGTH_OF_FIELDS_USER
    )
    last_name = CharField(
        'Фамилия',
        max_length=settings.LENGTH_OF_FIELDS_USER
    )
    email = EmailField(
        'Электронная почта',
        max_length=settings.LENGTH_OF_FIELDS_USER,
        unique=True
    )
    username = CharField(
        'Имя пользователя',
        max_length=settings.LENGTH_OF_FIELDS_USERNAME,
        unique=True,
        validators=[UnicodeUsernameValidator(
            message='Имя пользователя не соответсвует стандартам Unicode'
        )]
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.username


class Subscription(Model):
    """ Модель подписки. """

    user = ForeignKey(
        User,
        on_delete=CASCADE,
        verbose_name='Подписчик',
        related_name='subscriber'
    )
    author = ForeignKey(
        User,
        on_delete=CASCADE,
        verbose_name='Автор',
        related_name='author'
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['user', 'author'],
                name='subscription_unique'
            ),
            models.CheckConstraint(
                check=~Q(user=F('author')),
                name='self_follow'
            )
        ]

    def __str__(self):
        return f'{self.user} подписался на {self.author}'
