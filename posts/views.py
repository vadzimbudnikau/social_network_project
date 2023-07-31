from django.shortcuts import redirect, get_object_or_404
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from .models import Post, Comment, Like
from .forms import PostForm, CommentForm


class CreatePostView(LoginRequiredMixin, CreateView):
    """
    View for creating a new post.
    """
    model = Post
    template_name = 'posts/create_post.html'
    form_class = PostForm

    def form_valid(self, form):
        """
        Set the post author as the currently logged-in user before saving.
        """
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        """
        Return the URL to redirect after successful post creation.
        """
        return reverse_lazy('accounts:home')


class PostDetailView(DetailView):
    """
    View for displaying post details along with comments and likes.
    """
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        """
        Get additional context data for the post detail page.
        """
        context = super().get_context_data(**kwargs)
        post = self.object
        liked = Like.objects.filter(user=self.request.user, post=post).exists()
        context['liked'] = liked
        context['total_likes'] = post.like_set.count()
        context['comment_form'] = CommentForm()
        context['comments'] = post.comments.all().order_by('-created_at')
        return context

    def post(self, request, *args, **kwargs):
        """
        Handle the POST request for adding a new comment to the post.
        """
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.get_object()
            comment.author = self.request.user
            comment.save()
        return redirect('posts:post_detail', pk=self.get_object().pk)


class LikeToggleView(View):
    """
    View for toggling likes on a post.
    """

    def post(self, request, pk):
        """
        Handle the POST request for toggling likes on a post.
        """
        post = get_object_or_404(Post, pk=pk)

        if Like.objects.filter(user=request.user, post=post).exists():
            Like.objects.filter(user=request.user, post=post).delete()
        else:
            Like.objects.create(user=request.user, post=post)

        return redirect(reverse('posts:post_detail', args=[pk]))


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    View for updating a post. Only the author of the post can access this view.
    """
    model = Post
    template_name = 'posts/post_form.html'
    form_class = PostForm

    def test_func(self):
        """
        Check if the user is the author of the post.
        """
        return self.request.user == self.get_object().author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    View for deleting a post. Only the author of the post can access this view.
    """
    model = Post
    template_name = 'posts/post_confirm_delete.html'
    success_url = reverse_lazy('posts:post_list')

    def test_func(self):
        """
        Check if the user is the author of the post.
        """
        return self.request.user == self.get_object().author


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    View for updating a comment. Only the author of the comment can access this view.
    """
    model = Comment
    template_name = 'posts/comment_form.html'
    form_class = CommentForm

    def test_func(self):
        """
        Check if the user is the author of the comment.
        """
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        """
        Return the URL to redirect after successful comment update.
        """
        return reverse_lazy('posts:post_detail', kwargs={'pk': self.object.post.pk})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    View for deleting a comment. Only the author of the comment can access this view.
    """
    model = Comment
    template_name = 'posts/comment_confirm_delete.html'

    def test_func(self):
        """
        Check if the user is the author of the comment.
        """
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        """
        Return the URL to redirect after successful comment deletion.
        """
        post_pk = self.object.post.pk
        return reverse('posts:post_detail', args=[post_pk])

    def get_context_data(self, **kwargs):
        """
        Add extra context data for the comment delete confirmation page.
        """
        context = super().get_context_data(**kwargs)
        context['post'] = self.object.post
        return context
