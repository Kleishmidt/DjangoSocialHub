from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse
from utils.exception_handling import handle_exception


class Post(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(default=datetime.utcnow, editable=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images', default='default_image.png')
    likes = models.ManyToManyField(User, related_name='like_posts')

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
