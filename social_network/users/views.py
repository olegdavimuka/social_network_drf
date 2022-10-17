from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from users.serializers import SignUpSerializer, UserSerializer

from .permissions import (IsNotAuthenticated, IsOwnerOrRestricted,
                          IsStaffOrReadOnly)


class SignUpView(generics.CreateAPIView):
    """ """

    serializer_class = SignUpSerializer
    permission_classes = [IsNotAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                "message": "User Created Successfully",
            },
            status=status.HTTP_201_CREATED,
        )


class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions for users.
    """

    queryset = get_user_model().objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsStaffOrReadOnly,
        IsOwnerOrRestricted,
    ]

    def list(self, request, *args, **kwargs):
        """
        List all users.
        """

        if not request.user.is_staff:
            self.queryset = self.queryset.filter(id=request.user.id)
        return super().list(request, *args, **kwargs)


class UserActivity(APIView):
    """
    A viewset that provides the user activity data
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        user = get_user_model().objects.get(id=pk)
        return Response(
            {
                "last_login": user.last_login,
                "last_activity": user.last_activity,
            },
            status=status.HTTP_200_OK,
        )
