from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Post(models.Model):
    """
    Represents a single post created by a user.
    """

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=True, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, through='Like', related_name='liked_posts', blank=True)

    def __str__(self):
        return f'Post by {self.author.username} at {self.created_at}'

    def total_likes(self):
        """
        Returns the total number of likes for the post.
        """
        return self.likes.count()

    def get_absolute_url(self):
        """
        Returns the absolute URL for the post detail page.
        """
        return reverse('posts:post_detail', args=[str(self.id)])


class Comment(models.Model):
    """
    Represents a comment made by a user on a specific post.
    """

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'


class Like(models.Model):
    """
    Represents a like made by a user on a specific post.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} likes {self.post}"
