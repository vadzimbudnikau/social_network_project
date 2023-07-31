from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, UpdateView, CreateView, ListView
from .forms import UserProfileForm, CustomPasswordChangeForm
from .models import Profile
from posts.models import Post
from private_messages.models import Message


class PostListView(ListView):
    """
    View to display a list of posts.
    """
    model = Post
    template_name = 'accounts/home.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 3

    def get_queryset(self):
        """
        Return the queryset of posts filtered by search query.
        """
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(title__icontains=query) | Q(title__icontains=query.lower()))
        return queryset


class SignUpView(CreateView):
    """
    View for user registration (signup).
    """
    template_name = 'accounts/signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('accounts:home')

    def form_valid(self, form):
        """
        Save the form and log in the user after successful registration.
        """
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        profile = user.profile
        return redirect('accounts:profile', slug=profile.slug)


class CustomLoginView(LoginView):
    """
    Custom view for user login.
    """
    template_name = 'accounts/login.html'

    def get_success_url(self):
        """
        Get the success URL after login.
        """
        profile = self.request.user.profile
        return reverse_lazy('accounts:profile', kwargs={'slug': profile.slug})


class CustomLogoutView(LogoutView):
    """
    Custom view for user logout.
    """
    template_name = 'accounts/logout.html'
    next_page = '/login/'


class ProfileDetailView(LoginRequiredMixin, DetailView):
    """
    View for user profile detail.
    """
    template_name = 'accounts/profile.html'
    model = Profile
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        """
        Get the profile object based on the slug from the URL.
        """
        slug = self.kwargs.get('slug')
        return get_object_or_404(Profile, slug=slug)

    def get_context_data(self, **kwargs):
        """
        Add additional context data for the profile view, including followers and following counts.
        """
        context = super().get_context_data(**kwargs)
        user_profile = self.object
        context['slug'] = user_profile.slug
        context['followers_count'] = user_profile.followers_profiles.count()
        context['following_count'] = user_profile.following_profiles.count()

        # Добавим список входящих сообщений для текущего пользователя
        current_user = self.request.user
        if current_user.is_authenticated and current_user == user_profile.user:
            context['inbox'] = Message.objects.filter(recipient=current_user).order_by('-timestamp')
        return context


class EditProfileView(LoginRequiredMixin, UpdateView):
    """
    View for editing user profile.
    """
    template_name = 'accounts/edit_profile.html'
    form_class = UserProfileForm

    def get_object(self, queryset=None):
        """
        Get the profile object based on the slug from the URL.
        """
        slug = self.kwargs.get('slug')
        return get_object_or_404(Profile, slug=slug)

    def form_valid(self, form):
        """
        Save the form and set the user for the profile.
        """
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        """
        Get the success URL after editing the profile.
        """
        profile = self.request.user.profile
        return reverse_lazy('accounts:profile', kwargs={'slug': profile.slug})


class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    """
    View for changing user password.
    """
    template_name = 'accounts/change_password.html'
    form_class = CustomPasswordChangeForm

    def get_success_url(self):
        """
        Get the success URL after changing the password.
        """
        profile = self.request.user.profile
        return reverse_lazy('accounts:profile', kwargs={'slug': profile.slug})


class FollowView(View):
    """
    View for following another user.
    """

    def post(self, request, slug, *args, **kwargs):
        profile_to_follow = get_object_or_404(Profile, slug=slug)
        user_profile = request.user.profile

        if profile_to_follow == user_profile:
            return redirect('accounts:profile', slug=slug)

        user_profile.following.add(profile_to_follow)
        profile_to_follow.followers.add(user_profile)

        return redirect('accounts:profile', slug=slug)


class UnfollowView(View):
    """
    View for unfollowing another user.
    """

    def post(self, request, slug, *args, **kwargs):
        profile_to_unfollow = get_object_or_404(Profile, slug=slug)
        user_profile = request.user.profile

        user_profile.following.remove(profile_to_unfollow)
        profile_to_unfollow.followers.remove(user_profile)

        return redirect('accounts:profile', slug=slug)


class FollowersListView(ListView):
    """
    View for displaying a list of followers.
    """
    model = Profile
    template_name = 'accounts/followers_list.html'
    context_object_name = 'followers'

    def get_queryset(self):
        """
        Get the list of followers for the profile specified in the URL.
        """
        slug = self.kwargs.get('slug')
        profile = get_object_or_404(Profile, slug=slug)
        return profile.followers_profiles.all()


class FollowingListView(ListView):
    """
    View for displaying a list of following users.
    """
    model = Profile
    template_name = 'accounts/following_list.html'
    context_object_name = 'following'

    def get_queryset(self):
        """
        Get the list of following users for the profile specified in the URL.
        """
        slug = self.kwargs.get('slug')
        profile = get_object_or_404(Profile, slug=slug)
        return profile.following_profiles.all()
