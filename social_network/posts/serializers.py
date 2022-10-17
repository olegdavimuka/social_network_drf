from rest_framework import serializers

from .models import LikesDate, Post


class PostSerializer(serializers.ModelSerializer):
    """
    Define the Post API representation.
    """

    like_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "url",
            "title",
            "content",
            "like_count",
        )


class LikesDateSerializer(serializers.ModelSerializer):
    """
    Define the LikesDate API representation.
    """

    class Meta:
        model = LikesDate
        fields = (
            "date",
            "like_count",
        )
