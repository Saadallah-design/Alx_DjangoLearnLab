from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Post, Comment
from taggit.forms import TagWidget

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    #  adding a layer of security to ensure email uniqueness
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Registration failed. Please check your details and try again.")
        return email

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ["email"]

class ProfileForm(forms.ModelForm):
    # adding a security layer to validate profile picture uploads
    #  didn't use FileExtensionValidator since it only checks extensions, not actual content type or size
    def clean_profile_pic(self):
        profile_pic = self.cleaned_data.get('profile_pic')
        if profile_pic:
            if profile_pic.size > 2 * 1024 * 1024:  # 2MB limit
                raise forms.ValidationError("Profile picture size should not exceed 2MB.")
            if not profile_pic.content_type in ['image/jpeg', 'image/png', 'image/jpg']:
                raise forms.ValidationError("Only JPEG and PNG formats are supported.")
        return profile_pic
    
    class Meta:
        model = Profile
        fields = ["bio", "profile_pic"]

# post model form
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        widgets = {
            'tags': TagWidget(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Always set initial tags as comma-separated string for both create and update
        tags_qs = self.instance.tags.all() if self.instance.pk else []
        self.fields['tags'].initial = ', '.join(tag.name for tag in tags_qs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        tags = self.cleaned_data.get('tags')
        if commit:
            instance.save()
            instance.tags.set(tags)
        return instance

# Comment form
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class ReplyCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']