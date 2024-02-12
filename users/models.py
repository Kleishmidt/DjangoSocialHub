from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse

from utils.exception_handling import handle_exception


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.TextField(null=True)
    followers = models.ManyToManyField(User, related_name='following', blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    @handle_exception
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        max_dimension = 300
        if img.height > max_dimension or img.width > max_dimension:
            output_size = (max_dimension, max_dimension)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def get_absolute_url(self):
        return reverse('profile', kwargs={'pk': self.pk})
