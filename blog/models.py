from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse
from utils.exception_handling import handle_exception


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(default=datetime.utcnow, editable=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images', default='default_image')
    likes = models.ManyToManyField(User, related_name='like_posts')
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)

    def __str__(self):
        return f'Post by {self.author.username}'

    @handle_exception
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        max_dimension = 800
        if img.height > max_dimension or img.width > max_dimension:
            output_size = (max_dimension, max_dimension)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=datetime.utcnow, editable=False)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post}'
