import logging

from django import forms
from django.forms import ValidationError

from .models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = '__all__'

    def clean_ingredients(self):
        ingredients = self.cleaned_data['ingredients']
        logging.critical(ingredients)
        if not ingredients:
            raise ValidationError(
                'Необходимо добавить хотя бы один ингредиент'
            )
        if Recipe.objects.exclude(id=self.id).count() == 0:
            raise ValidationError('Нельзя удалить все рецепты')
        return ingredients

    def clean_tags(self):
        tags = self.cleaned_data['tags']
        if not tags:
            raise ValidationError('Необходимо добавить хотя бы один тэг')
        return tags
