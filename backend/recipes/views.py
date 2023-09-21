from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from users.permissions import IsAuthorOrReadOnly
from .filters import IngredientFilter, RecipeFilter
from .mixins import ModelMixin
from .models import Favorite, Ingredient, Recipe, ShoppingList, Tag
from .pagination import SimplePagination
from .serializers import (CreateRecipeSerializer, FavoriteSerializer,
                          IngredientSerializer, RecipeSerializer,
                          ShoppingListSerializer, TagSerializer)
from .utils import download_shopping_list


class RecipeViewSet(viewsets.ModelViewSet):
    """ Отображение рецептов. """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = RecipeFilter
    pagination_class = SimplePagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return CreateRecipeSerializer
        return RecipeSerializer

    @action(detail=True, methods=['POST', 'DELETE'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        """ Добавление/удаление рецепта из избранного. """
        serializer = FavoriteSerializer
        return ModelMixin().add_del_recipe(request, pk, serializer, Favorite)

    @action(detail=True, methods=['POST', 'DELETE'],
            permission_classes=[IsAuthenticated],)
    def shopping_cart(self, request, pk):
        """ Добавление/удаление рецепта из списка покупок. """
        serializer = ShoppingListSerializer
        return ModelMixin().add_del_recipe(
            request, pk, serializer, ShoppingList
        )

    @action(detail=False, permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        """ Скачать список покупок. """
        try:
            return download_shopping_list(request)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """ Отображение ингредиентов. """

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filter_backends = (IngredientFilter,)
    search_fields = ['^name', ]


class TagViewSet(viewsets.ModelViewSet):
    """ Отображение тегов. """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
