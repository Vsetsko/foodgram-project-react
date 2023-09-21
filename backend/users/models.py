from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db.models import (CASCADE, CharField, EmailField, ForeignKey,
                              Model, UniqueConstraint)


class User(AbstractUser):
    """ Модель пользователя. """

    first_name = CharField(
        'Имя',
        max_length=50
    )
    last_name = CharField(
        'Фамилия',
        max_length=50
    )
    email = EmailField(
        'Электронная почта',
        max_length=128,
        unique=True
    )
    username = CharField(
        'Имя пользователя',
        max_length=128,
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
            )
        ]

    def __str__(self):
        return f'{self.user} подписался на {self.author}'
