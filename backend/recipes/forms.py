from django import forms
from django.forms import ValidationError

from .models import Recipe


class RecipeForm(forms.ModelForm):
    def clean(self):
        if not self.ingredients.exists():
            raise ValidationError(
                'Необходимо добавить хотя бы один ингредиент'
            )
        if not self.tags.exists():
            raise ValidationError('Необходимо добавить хотя бы один тэг')
        if Recipe.objects.exclude(id=self.id).count() == 0:
            raise ValidationError('Нельзя удалить все рецепты')
