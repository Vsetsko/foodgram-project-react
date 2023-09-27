from djoser.serializers import UserSerializer
from rest_framework import serializers, status
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from recipes.models import Recipe
from .models import Subscription, User


class CustomUserSerializer(ModelSerializer):
    """ Сериализатор пользователя. """

    is_subscribed = SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name',
            'last_name', 'is_subscribed'
        ]

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        return (
            not user.is_anonymous
            and user.subscriber.filter(author=obj).exists()
        )


class CropRecipeSerializer(ModelSerializer):
    """ Укороченный сериализатор рецепта. """

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'image', 'cooking_time']
        read_only_fields = ['__all__', ]


class SubscribeSerializer(CustomUserSerializer):
    """ Сериализатор подписки. """

    recipes = SerializerMethodField()
    recipes_count = SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['recipes', 'recipes_count']
        read_only_fields = ['email', 'username', 'first_name', 'last_name']

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        return (not user.is_anonymous
                and user.subscriber.filter(author=obj).exists())

    def get_recipes(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        recipes = obj.recipes.all()
        limit = request.query_params.get('recipes_limit')
        if limit:
            try:
                recipes = recipes[:int(limit)]
            except ValueError:
                pass
        return CropRecipeSerializer(recipes, many=True,
                                    context={'request': request}).data

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class SubscriptionSerializer(ModelSerializer):
    class Meta:
        model = Subscription
        fields = [
            'user',
            'author',
        ]

    def validate(self, data):
        author = data['author']
        user = data['user']
        if author.subscribers.filter(user=user).exists():
            raise serializers.ValidationError(
                'Вы уже подписаны',
                code=status.HTTP_400_BAD_REQUEST
            )
        if user == author:
            raise serializers.ValidationError(
                'Запрещено подписываться на себя',
                code=status.HTTP_400_BAD_REQUEST
            )
        return data
