from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import logout
from allauth.socialaccount.models import SocialToken

from utils.exception_handling import handle_exception
from blog.models import Post
from .models import Profile
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


@handle_exception
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def custom_logout(request):
    try:
        google_token = SocialToken.objects.get(account__user=request.user, account__provider='google')
        google_token.token = None
        google_token.token_secret = None
        google_token.save()
    except SocialToken.DoesNotExist:
        pass

    try:
        github_token = SocialToken.objects.get(account__user=request.user, account__provider='github')
        github_token.token = None
        github_token.token_secret = None
        github_token.save()
    except SocialToken.DoesNotExist:
        pass

    logout(request)
    return render(request, 'users/logout.html')


def delete_profile(request, profile):
    profile.delete()
    request.user.delete()
    return redirect('/')


def update_profile(request, profile):
    u_form = UserUpdateForm(request.POST, instance=request.user)
    p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
    if u_form.is_valid() and p_form.is_valid():
        u_form.save()
        p_form.save()
        messages.success(request, f'Your account has been updated!')
        return redirect(reverse('profile', args=[profile.id]))


def profile(request, *args, **kwargs):
    profile = Profile.objects.filter(pk=kwargs['pk']).first()
    posts = Post.objects.filter(author=profile.user).order_by('-created_at')
    followers = profile.followers.all
    follows = profile.user.following.count()
    u_form = UserUpdateForm(instance=request.user)
    p_form = ProfileUpdateForm(instance=request.user.profile)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'follow':
            profile.followers.add(request.user)
        elif action == 'unfollow':
            profile.followers.remove(request.user)
        elif action == 'delete':
            return delete_profile(request, profile)
        elif action == 'update':
            return update_profile(request, profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'posts': posts,
        'profile': profile,
        'followers': followers,
        'follows': follows,
    }

    return render(request, 'users/profile.html', context)
