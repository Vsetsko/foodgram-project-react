from django.db.models import (CASCADE, CharField, DateTimeField, ForeignKey,
                              ImageField, ManyToManyField, Model,
                              PositiveSmallIntegerField, SlugField, TextField,
                              UniqueConstraint)

from users.models import User


class Ingredient(Model):
    """ Модель ингредиента. """

    name = CharField('Название ингредиента', max_length=200)
    measurement_unit = CharField('Единица измерения', max_length=20)

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


class Tag(Model):
    """ Модель тега """

    name = CharField('Название тега', max_length=22)
    color = CharField('HEX-код цвета', max_length=7)
    slug = SlugField('Slug', unique=True, max_length=200)

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
    name = CharField('Название рецепта', max_length=200)
    image = ImageField('Изображение', upload_to='recipes/images/')
    text = TextField('Описание', max_length=500)
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
    cooking_time = PositiveSmallIntegerField('Время приготовления')
    created = DateTimeField('Дата и время создания', auto_now_add=True)

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
    amount = PositiveSmallIntegerField('Количество ингредиентов')

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='recipe_ingredient_unique'
            )
        ]


class RecipeTag(Model):
    """ Модель связи рецепта и тега. """

    recipe = ForeignKey(
        Recipe,
        on_delete=CASCADE,
        verbose_name='Рецепт'
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
