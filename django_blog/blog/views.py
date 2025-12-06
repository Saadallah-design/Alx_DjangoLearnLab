"""
Django Blog App - Feature Overview

Features:
1. List all posts (public)
2. View post details (public)
3. Create post (authenticated users only)
    - Author set automatically to logged-in user
4. Edit post (only by original author)
5. Delete post (only by original author)

Permissions & Data Handling:
- Only logged-in users can create, edit, or delete posts
- Users can only modify their own posts
- Author is set in the backend, not via the form
- All forms use CSRF protection
- Posts ordered by newest first

See README.md for more details.
"""
from asyncio.log import logger
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, PostForm, CommentForm, ReplyCommentForm
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView
from .models import Post, Profile, Comment
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q

def register(request):
    # URL: /register/
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully. You can now log in.')
            return redirect('login')
    else:
        messages.error(request, "Registration failed. Please check your details.")
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})


# Profile view: view and edit email, bio, and profile_pic
from .forms import UserUpdateForm, ProfileForm


@login_required
def profile(request):
    # URL: /profile/
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = ProfileForm(instance=profile)
    return render(request, 'blog/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

# defining views for post management (create, edit, delete)



# to restrict user actions based on login status and ownership of posts
# in class based views use LoginRequiredMixin. 
class PostCreateView(LoginRequiredMixin, CreateView):
    # URL: /posts/new/
    model = Post
    form_class = PostForm
    # since using form_class, no need to specify fields here
    # fields = ['title', 'content']
    template_name = 'blog/post_form.html'
    # success_url = reverse_lazy('home') # no more needed since we override get_success_url

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Your post has been created successfully.')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.pk})
    
# UserPassesTestMixin to ensure only authors can edit or delete their posts
# custom permission logic in test_func method. when used we can define test_func method
# It lets you define a test_func method: only users for whom this method returns True can access the view.
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    # URL: /posts/<int:pk>/edit/
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('home')

    # test_func to ensure only author can edit
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Your post has been updated successfully.')
        return super().form_valid(form)
    
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    # URL: /posts/<int:pk>/delete/
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('home')

    # test_func to ensure only author can delete
    def test_func(self):
        post = self.get_object()
        messages.success(self.request, 'Your post has been deleted successfully.')
        return self.request.user == post.author
    
class PostListView(ListView):
    # URL: /posts/
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
    paginate_by = 5

class PostDetailView(DetailView):
    # URL: /posts/<int:pk>/
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        context['comment_form'] = CommentForm()
        context['tags'] = self.object.tags.all()
        return context

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/add_comment.html'

    def form_valid(self, form):
        post_pk = self.kwargs.get('pk')
        post = get_object_or_404(Post, pk=post_pk)
        form.instance.post = post
        form.instance.author = self.request.user
        messages.success(self.request, 'Your comment has been added.')
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.post.get_absolute_url()

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['content']
    template_name = 'blog/comment_form.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return self.object.post.get_absolute_url()

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return self.object.post.get_absolute_url()

class ReplyCommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = ReplyCommentForm
    template_name = 'blog/reply_comment_form.html'

    def form_valid(self, form):
        parent_comment = get_object_or_404(Comment, pk=self.kwargs.get('pk'))
        post = parent_comment.post
        form.instance.post = post
        form.instance.author = self.request.user
        form.instance.parent = parent_comment
        messages.success(self.request, 'Your reply has been added.')
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.post.get_absolute_url()
    

# filter posts by tag
class PostsByTagListView(ListView):
    model = Post
    template_name = 'blog/posts_by_tag.html'
    context_object_name = 'posts'

    def get_queryset(self):
        tag_name = self.kwargs.get('tag_name')
        return Post.objects.filter(tags__name=tag_name)

# Search view for posts by title, content, or tags
def search_posts(request):
    query = request.GET.get('q', '').strip().lower()
    results = []
    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
    return render(request, 'blog/search_results.html', {'query': query, 'results': results})