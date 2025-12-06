# Django Blog Comments: Theory, Mistakes, Best Practices, and Code Examples

---

## Theory: Threaded Comments in Django

Threaded (nested) comments allow users to reply to other comments, creating a discussion tree. Each comment can have a parent (another comment) or be a top-level comment. This is achieved by adding a `parent` field to the `Comment` model:

```python
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # ...
```

---

## Common Mistakes

1. **Not running migrations after model changes**
   - Always run `makemigrations` and `migrate` after adding fields.
2. **Incorrect URL patterns and template arguments**
   - If your URL expects both `post_id` and `comment_id`, always pass both in `{% url %}`.
   - Example mistake: `{% url 'comment_edit' comment.pk %}` (should be `{% url 'comment_edit' post.pk comment.pk %}`)
3. **Not handling permissions**
   - Always check that only the comment author can edit/delete their comment.
4. **Exposing author/post fields in forms**
   - Set these in the view, not in the form.
5. **Not using generic views where possible**
   - Use Django’s `CreateView`, `UpdateView`, `DeleteView` for maintainability.
6. **Not displaying messages to users**
   - Use Django’s messages framework and show them in templates.

---

## Best Practices

- **RESTful URLs:**
  - `/posts/<int:post_id>/comments/new/` for adding
  - `/posts/<int:post_id>/comments/<int:comment_id>/edit/` for editing
  - `/posts/<int:post_id>/comments/<int:comment_id>/delete/` for deleting
  - `/posts/<int:post_id>/comments/<int:comment_id>/reply/` for replying
- **Use generic views:**
  - Example:
    ```python
    class CommentCreateView(LoginRequiredMixin, CreateView):
        model = Comment
        form_class = CommentForm
        # ...
    ```
- **Permission checks:**
  - Use `LoginRequiredMixin` and `UserPassesTestMixin`.
  - Example:
    ```python
    class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
        def test_func(self):
            return self.request.user == self.get_object().author
    ```
- **Set author/post in view:**
  - Example:
    ```python
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        # ...
    ```
- **Show messages in templates:**
  - Example:
    ```html
    {% if messages %}
      <ul class="messages">
        {% for message in messages %}
          <li class="message {{ message.tags }}">{{ message }}</li>
        {% endfor %}
      </ul>
    {% endif %}
    ```
- **Style and auto-hide messages:**
  - Use CSS and JS in static files for maintainability.
- **Display replies nested under parent comments:**
  - Example:
    ```django
    {% for comment in comments %}
      ...
      {% for reply in comment.replies.all %}
        <div class="reply">{{ reply.content }}</div>
      {% endfor %}
    {% endfor %}
    ```

---

## Code Examples

### Models
```python
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # ...
```

### Forms
```python
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
```

### Views
```python
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/add_comment.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        parent_id = self.kwargs.get('comment_id')
        if parent_id:
            form.instance.parent = get_object_or_404(Comment, pk=parent_id)
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.post.get_absolute_url()
```

### URLs
```python
urlpatterns = [
    path('posts/<int:post_id>/comments/new/', views.CommentCreateView.as_view(), name='add_comment'),
    path('posts/<int:post_id>/comments/<int:comment_id>/edit/', views.CommentUpdateView.as_view(), name='comment_edit'),
    path('posts/<int:post_id>/comments/<int:comment_id>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),
    path('posts/<int:post_id>/comments/<int:comment_id>/reply/', views.ReplyCommentCreateView.as_view(), name='reply_comment'),
]
```

### Templates
```django
{% for comment in comments %}
  <div class="comment">
    <strong>{{ comment.author.username }}</strong>
    <span>{{ comment.content }}</span>
    {% if user.is_authenticated %}
      <a href="{% url 'reply_comment' post.pk comment.pk %}">Reply</a>
    {% endif %}
    {% for reply in comment.replies.all %}
      <div class="reply">{{ reply.content }}</div>
    {% endfor %}
  </div>
{% endfor %}
```

---

## Summary
- Always keep URLs RESTful and intuitive.
- Use generic views and permission mixins.
- Set sensitive fields in views, not forms.
- Run migrations after model changes.
- Pass all required arguments in `{% url %}` tags.
- Display and style messages for user feedback.
- Show replies nested under parent comments.

This approach ensures your comment system is secure, maintainable, and user-friendly.
