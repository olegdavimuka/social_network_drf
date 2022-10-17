from django.db import models
from users.models import User


class Post(models.Model):
    """
    Define the Post model.
    """

    title = models.CharField(max_length=32)
    content = models.TextField(max_length=256)
    like_count = models.IntegerField(default=0)
    liked_by = models.ManyToManyField(User, related_name="liked_posts")
    like_date = models.DateField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Title: {self.title}, \
                Content: {self.content}, \
                Like Count: {self.like_count}"


class LikesDate(models.Model):
    """
    Define the LikesDate model.
    """

    date = models.DateField(unique=True)
    like_count = models.IntegerField(default=0)

    def __str__(self):
        return f"Date: {self.date}, Like Count: {self.like_count}"
