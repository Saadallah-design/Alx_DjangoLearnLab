# Django Authentication System: Detailed Documentation

This document explains how the authentication system in this Django blog project works, describes each part of the process, and provides instructions for testing all authentication features.

---

## 1. Overview: How Authentication Works in Django
- **Authentication** is the process of verifying a user's identity (login/logout).
- **Authorization** is the process of checking what an authenticated user is allowed to do (permissions).
- Django provides built-in views, forms, and models for authentication, which are used and extended in this project.

---

## 2. Components and Flow

### a. User Model
- Uses Django’s built-in `User` model (`django.contrib.auth.models.User`).
- Stores username, email, password (hashed), and other info.


**View (views.py):**
```python
from .forms import CustomUserCreationForm
from django.shortcuts import render, redirect

def register(request):
	if request.method == 'POST':
		form = CustomUserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('login')
	else:
		form = CustomUserCreationForm()
	return render(request, 'registration/register.html', {'form': form})
```

**Form (forms.py):**
```python
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def clean_email(self):
		email = self.cleaned_data.get('email')
		if User.objects.filter(email=email).exists():
			raise forms.ValidationError("Registration failed. Please check your details and try again.")
		return email
```

**Template (registration/register.html):**
```django
{% extends 'base.html' %}
{% block content %}
<h2>Register</h2>
<form method="post">
	{% csrf_token %}
	{{ form.as_p }}
	<button type="submit">Register</button>
</form>
{% endblock %}
```


**URL (urls.py):**
```python
from django.contrib.auth import views as auth_views
urlpatterns = [
	path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
]
```

**Template (registration/login.html):**
```django
{% extends 'base.html' %}
{% block content %}
<h2>Login</h2>
<form method="post">
	{% csrf_token %}
	{{ form.as_p }}
	<button type="submit">Login</button>
</form>
{% endblock %}
```


**URL (urls.py):**
```python
from django.contrib.auth import views as auth_views
urlpatterns += [
	path('logout/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),
]
```

**Template (registration/logged_out.html):**
```django
{% extends 'base.html' %}
{% block content %}
<h2>Logged out</h2>
<p>You have been logged out.</p>
{% endblock %}
```


**Model (models.py):**
```python
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	bio = models.TextField(blank=True)
	profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
```

**Form (forms.py):**
```python
from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
	def clean_profile_pic(self):
		profile_pic = self.cleaned_data.get('profile_pic')
		if profile_pic:
			if profile_pic.size > 2 * 1024 * 1024:
				raise forms.ValidationError("Profile picture size should not exceed 2MB.")
			if not profile_pic.content_type in ['image/jpeg', 'image/png', 'image/jpg']:
				raise forms.ValidationError("Only JPEG and PNG formats are supported.")
		return profile_pic
	class Meta:
		model = Profile
		fields = ["bio", "profile_pic"]
```

**View (views.py):**
```python
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileForm

@login_required
def profile(request):
	user = request.user
	if request.method == 'POST':
		user_form = UserUpdateForm(request.POST, instance=user)
		profile_form = ProfileForm(request.POST, request.FILES, instance=user.profile)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			return redirect('profile')
	else:
		user_form = UserUpdateForm(instance=user)
		profile_form = ProfileForm(instance=user.profile)
	return render(request, 'registration/profile.html', {
		'user_form': user_form,
		'profile_form': profile_form
	})
```

**Template (registration/profile.html):**
```django
{% extends 'base.html' %}
{% block content %}
<h2>Profile</h2>
<form method="post" enctype="multipart/form-data">
	{% csrf_token %}
	<p><strong>Username:</strong> {{ user.username }}</p>
	{{ user_form.email.label_tag }} {{ user_form.email }}<br><br>
	{{ profile_form.bio.label_tag }}<br>{{ profile_form.bio }}<br><br>
	{% if user.profile.profile_pic %}
		<img src="{{ user.profile.profile_pic.url }}" alt="Profile Picture" width="120"><br>
	{% endif %}
	{{ profile_form.profile_pic.label_tag }} {{ profile_form.profile_pic }}<br><br>
	<button type="submit">Update Profile</button>
</form>
<p><a href="{% url 'logout' %}">Logout</a></p>
{% endblock %}
```

### f. Password Management (if enabled)
- Django provides built-in views for password reset and change.

---

## 3. How Users Interact
- **Register:** Go to `/register/`, fill out the form, and submit.
- **Login:** Go to `/login/`, enter credentials, and submit.
- **Logout:** Go to `/logout/` or click the logout link.
- **Profile:** Go to `/profile/` to view or edit your info (must be logged in).

---

## 4. Security Features
- **CSRF protection:** All forms include `{% csrf_token %}`.
- **Password hashing:** Passwords are never stored in plain text.
- **Rate limiting:** (Recommended) Add to login, registration, and password reset views.
- **Generic error messages:** Prevents leaking info about registered emails/usernames.
- **File upload validation:** Only images (JPEG/PNG) under 2MB are accepted for profile pictures.

---

## 5. How to Test Each Feature

### a. Registration
1. Go to `/register/`.
2. Try registering with a new username/email (should succeed).
3. Try registering with an existing email (should show a generic error).

### b. Login
1. Go to `/login/`.
2. Enter valid credentials (should log in and redirect to profile).
3. Enter invalid credentials (should show a generic error).

### c. Logout
1. Click the logout link or go to `/logout/`.
2. You should be logged out and see a confirmation page.

### d. Profile Management
1. Log in and go to `/profile/`.
2. Edit your email, bio, or upload a profile picture (JPEG/PNG, <2MB).
3. Try uploading a large or invalid file (should show an error).

### e. Rate Limiting (if enabled)
1. Try logging in or registering repeatedly in a short time.
2. After exceeding the limit, you should see an error (HTTP 429 or custom message).

### f. Password Reset (if enabled)
1. Go to `/password_reset/` and follow the instructions.
2. Check your email for the reset link (if email backend is configured).

---

## 6. Best Practices
- Always use HTTPS in production.
- Use strong, unique passwords.
- Log out after using public computers.
- Never share your credentials.

---

For more, see the [Django authentication docs](https://docs.djangoproject.com/en/stable/topics/auth/default/).
