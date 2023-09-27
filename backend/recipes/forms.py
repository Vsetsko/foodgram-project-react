from django import forms
from django.forms import ValidationError

from .models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data['ingredients']:
            raise ValidationError(
                'Необходимо добавить хотя бы один ингредиент'
            )
        if not cleaned_data['tags']:
            raise ValidationError('Необходимо добавить хотя бы один тэг')
        if Recipe.objects.exclude(id=self.id).count() == 0:
            raise ValidationError('Нельзя удалить все рецепты')
        return cleaned_data
