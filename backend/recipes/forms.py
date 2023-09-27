from django import forms

from .models import Recipe


class RecipeForm(forms.ModelForm):
    def clean(self):
        if not self.ingredients.exists():
            raise ValueError('Необходимо добавить хотя бы один ингредиент')
        if not self.tags.exists():
            raise ValueError('Необходимо добавить хотя бы один тэг')
        if Recipe.objects.exclude(id=self.id).count() == 0:
            raise ValueError('Нельзя удалить все рецепты')
