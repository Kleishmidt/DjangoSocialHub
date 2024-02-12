from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import ListView, CreateView

from .forms import PostForm
from .models import Post
from utils.exception_handling import handle_exception


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 3

    def post(self, request, *args, **kwargs):
        pk = request.POST.get('post_id')
        action = request.POST.get('action')
        post = get_object_or_404(Post, pk=pk)
        if action == 'like':
            post.likes.add(request.user)
        elif action == 'unlike':
            post.likes.remove(request.user)
        return redirect(reverse('blog-home'))


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['content', 'image']

    @handle_exception
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


@handle_exception
def delete(request, post):
    post.delete()
    return redirect('/')


def update(request, post, template_name):
    form = PostForm(request.POST, request.FILES, instance=post)
    if form.is_valid():
        form.save()
        return redirect(reverse('post-detail', args=[post.id]))
    return render(request, template_name, {'post': post, 'form': form})


def view_post(request, *args, **kwargs):
    post = Post.objects.get(pk=kwargs['pk'])
    form = PostForm(instance=post)
    template_name = 'blog/post_detail.html'
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'like':
            post.likes.add(request.user)
        elif action == 'unlike':
            post.likes.remove(request.user)
        elif action == 'update':
            return update(request, post, template_name)
        elif action == 'delete':
            return delete(request, post)
    return render(request, template_name, {'post': post, 'form': form})


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
