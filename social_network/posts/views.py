from datetime import datetime

from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import LikesDate, Post
from .serializers import LikesDateSerializer, PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows posts to be viewed or edited.
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = PostSerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data)


class PostLikeView(APIView):
    """
    API endpoint that allows posts to be liked.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        user = request.user
        now = datetime.now()

        if user not in post.liked_by.all():
            post.liked_by.add(user)
            post.like_count += 1
            post.like_date = now.date()
            post.save()

            date, _ = LikesDate.objects.get_or_create(date=now.date())
            date.like_count += 1
            date.save()

            user.last_activity = now
            user.save()

            return Response(
                {"message": "Post liked successfully."},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"message": "You already liked this post."},
                status=status.HTTP_200_OK,
            )


class PostUnlikeView(APIView):
    """
    API endpoint that allows posts to be unliked.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        user = request.user
        now = datetime.now()
        like_date = post.like_date

        if user in post.liked_by.all():
            post.liked_by.remove(user)
            post.like_count -= 1
            post.like_date = None
            post.save()

            date = LikesDate.objects.get(date=like_date)
            date.like_count -= 1
            date.save()
            if date.like_count == 0:
                date.delete()

            user.last_activity = now
            user.save()

            return Response(
                {"message": "Post unliked successfully."},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"message": "You didn't like this post."},
                status=status.HTTP_200_OK,
            )


class AnalyticsView(APIView):
    """
    API endpoint that allows to get analytics for likes count per day.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        from_date = request.query_params.get("from_date", datetime.now().date())
        to_date = request.query_params.get("to_date", datetime.now().date())
        dates = LikesDate.objects.all()
        dates = dates.filter(date__gte=from_date, date__lte=to_date)
        serializer = LikesDateSerializer(dates, many=True)
        return Response(serializer.data)
