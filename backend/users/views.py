from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ListSerializer

from recipes.pagination import SimplePagination
from .models import Subscription, User
from .serializers import SubscribeSerializer


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
        subscriber = request.user

        if request.method == 'POST':
            serializer = SubscribeSerializer(
                context=self.get_serializer_context()
            )
            serializer(Subscription.objects.get_or_create(
                user=subscriber,
                author=author
            )).save()
            return Response(serializer.to_representation(
                instance=author),
                status=status.HTTP_201_CREATED
            )
        Subscription.objects.filter(
            user=subscriber, author=author
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['GET'],
            permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        queryset = User.objects.filter(author__user=request.user)
        authors = self.paginate_queryset(queryset)
        serializer = ListSerializer(
            child=SubscribeSerializer(),
            context=self.get_serializer_context()
        )
        return self.get_paginated_response(
            serializer.to_representation(authors)
        )
