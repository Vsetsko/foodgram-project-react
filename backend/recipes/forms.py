from django.forms import BaseInlineFormSet, ValidationError


class IngredientTagInLineFormset(BaseInlineFormSet):
    def clean(self):
        data = self.cleaned_data
        for obj in reversed(data):
            if not obj or obj['DELETE'] is True:
                data.pop(data.index(obj))
        if not data:
            raise ValidationError(
                'Должен быть хотя бы один тег или ингредиент'
            )
        return super().clean()
