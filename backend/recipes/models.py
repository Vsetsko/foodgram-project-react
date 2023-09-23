from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import (CASCADE, CharField, DateTimeField, ForeignKey,
                              ImageField, ManyToManyField, Model,
                              PositiveSmallIntegerField, SlugField, TextField,
                              UniqueConstraint)

from users.models import User
from validators import validate_hex


class Ingredient(Model):
    """ Модель ингредиента. """

    name = CharField(
        settings.ENTER_INGREDIENT_NAME,
        max_length=settings.MAX_LENGTH_INGREDIENT_NAME
    )
    measurement_unit = CharField(
        settings.ENTER_UNIT, max_length=settings.MAX_LENGTH_INGREDIENT_UNIT
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='ingredient_unique'
            )
        ]

    def __str__(self) -> str:
        return f"{self.name} {self.measurement_unit}"


class Tag(Model):
    """ Модель тега """

    name = CharField(settings.ENTER_TAG,
                     max_length=settings.MAX_LENGTH_TAG_NAME)
    color = CharField(
        settings.ENTER_HEX,
        max_length=settings.MAX_LENGTH_TAG_COLOR, validators=[validate_hex]
    )
    slug = SlugField(settings.ENTER_SLUG, unique=True,
                     max_length=settings.MAX_LENGTH_TAG_SLUG)

    class Meta:
        ordering = ['name']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(Model):
    """ Модель рецепта """

    author = ForeignKey(
        User,
        on_delete=CASCADE,
        verbose_name='Автор рецепта',
        related_name='recipes'
    )
    name = CharField(settings.ENTER_INGREDIENT_NAME,
                     max_length=settings.MAX_LENGTH_RECIPE_NAME)
    image = ImageField(settings.ENTER_IMAGE, upload_to='recipes/images/')
    text = TextField(settings.ENTER_DESCRIPTION)
    ingredients = ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='Ингредиенты',
        related_name='ingredients'
    )
    tags = ManyToManyField(
        Tag,
        through='RecipeTag',
        verbose_name='Теги',
        related_name='tags'
    )
    cooking_time = PositiveSmallIntegerField(
        settings.ENTER_COOKING_TIME, validators=[
            MaxValueValidator(settings.MAX_VALUE_COOKING_TIME),
            MinValueValidator(settings.MIN_VALUE_COOKING_TIME)
        ]
    )
    created = DateTimeField(settings.ENTER_TIME_CREATION, auto_now_add=True)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-created']

    def __str__(self):
        return self.name


class RecipeIngredient(Model):
    """ Модель связи рецепта и ингредиента. """

    recipe = ForeignKey(
        Recipe,
        on_delete=CASCADE,
        verbose_name='Рецепт',
        related_name='recipe_ingredients'
    )
    ingredient = ForeignKey(
        Ingredient,
        on_delete=CASCADE,
        verbose_name='Ингредиент',
        related_name='recipe_ingredients'
    )
    amount = PositiveSmallIntegerField(settings.ENTER_QUANTITY_INGREDIENTS)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='recipe_ingredient_unique'
            )
        ]

    def __str__(self) -> str:
        return f"{self.recipe} {self.ingredient}"


class RecipeTag(Model):
    """ Модель связи рецепта и тега. """

    recipe = ForeignKey(
        Recipe,
        on_delete=CASCADE,
        verbose_name='Рецепт',
        related_name='recipe_tag'
    )
    tag = ForeignKey(
        Tag,
        on_delete=CASCADE,
        verbose_name='Тег'
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['recipe', 'tag'],
                name='recipe_tag_unique'
            )
        ]

    def __str__(self) -> str:
        return f"{self.recipe} {self.tag}"


class Favorite(Model):
    """ Модель избранного. """

    user = ForeignKey(
        User,
        on_delete=CASCADE,
        verbose_name='Пользователь',
        related_name='favorites'
    )
    recipe = ForeignKey(
        Recipe,
        on_delete=CASCADE,
        verbose_name='рецепт',
        related_name='favorites'
    )

    class Meta:
        verbose_name = 'Избранный'
        verbose_name_plural = 'Избранные'
        constraints = [
            UniqueConstraint(
                fields=['user', 'recipe'],
                name='favorite_unique'
            )
        ]

    def __str__(self) -> str:
        return f"{self.user} -> {self.recipe}"


class ShoppingList(Model):
    """ Модель списка покупок. """

    user = ForeignKey(
        User,
        on_delete=CASCADE,
        verbose_name='Пользователь',
        related_name='shopping'
    )
    recipe = ForeignKey(
        Recipe,
        on_delete=CASCADE,
        verbose_name='Рецепт',
        related_name='shopping'
    )

    class Meta:
        verbose_name = 'Список покупки'
        verbose_name_plural = 'Список покупок'
        constraints = [
            UniqueConstraint(
                fields=['user', 'recipe'],
                name='shopping_unique'
            )
        ]

    def __str__(self) -> str:
        return f"{self.user} -> {self.recipe}"
