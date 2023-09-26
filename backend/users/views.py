from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ListSerializer

from recipes.pagination import SimplePagination
from .models import Subscription, User
from .serializers import SubscribeSerializer, SubscriptionSerializer


class UserViewSet(UserViewSet):
    queryset = User.objects.all()
    pagination_class = SimplePagination

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, id):
        author = get_object_or_404(User, id=id)

        if request.method == 'POST':
            serializer = SubscriptionSerializer(
                context=self.get_serializer_context()
            )
            serializer.is_valid(raise_exception=True)
            serializer().save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        Subscription.objects.filter(
            user=request.user, author=author
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['GET'],
            permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        queryset = User.objects.filter(author__user=request.user)
        authors = self.paginate_queryset(queryset)
        serializer = ListSerializer(
            child=SubscribeSerializer(authors),
            context=self.get_serializer_context(),
        )
        return self.get_paginated_response(serializer.data)
