from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Post


class BlogAppTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.post = Post.objects.create(content='Test content', author=self.user)
        self.client.login(username='testuser', password='testpassword')

    def test_home_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/home.html')

    def test_post_detail_view(self):
        response = self.client.get(f'/post/{self.post.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_detail.html')

    def test_post_create_view(self):
        response = self.client.post('/post/new/', {'content': 'Test content'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.count(), 2)

