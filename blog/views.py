from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import ListView, CreateView

from .forms import PostForm, CommentForm
from .models import Post, Tag
from utils.exception_handling import handle_exception


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 5

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
    form_class = PostForm

    @handle_exception
    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        return response


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
    post = get_object_or_404(Post, pk=kwargs['pk'])
    form = PostForm(instance=post)
    comment_form = CommentForm()
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
        elif action == 'comment':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.post = post
                new_comment.author = request.user
                new_comment.save()
                return redirect(reverse('post-detail', args=[post.pk]))
    comments = post.comments.all()

    return render(request, template_name, {
        'post': post,
        'comment_form': comment_form,
        'comments': comments,
        'form': form,
    })


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


def search(request):
    query = request.GET.get('q')
    if query:
        tag = Tag.objects.filter(name__iexact=query).first()
        posts = tag.posts.all() if tag else Post.objects.none()

        users = User.objects.filter(username__icontains=query)
        profiles = []
        for user in users:
            profiles.append(user.profile)

        context = {
            'posts': posts,
            'profiles': profiles,
            'query': query,
        }
    else:
        context = {}
    return render(request, 'blog/search_results.html', context)
