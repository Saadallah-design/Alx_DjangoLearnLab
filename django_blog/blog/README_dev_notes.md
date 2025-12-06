
# Django Blog App - Developer Notes

## Overview
This document summarizes all major additions, fixes, and lessons learned during recent development of the Django blog app. It is intended to help current and future developers understand the project’s evolution, common pitfalls, and best practices.

---

## 1. User Profile Handling
- **Automatic Profile Creation:**
	- A `Profile` model extends the built-in `User` model with additional fields (bio, profile_pic).
	- A Django signal (`post_save` on `User`) ensures a `Profile` is created for every new user.
	- The signal is registered in `apps.py` using the `ready()` method, and `INSTALLED_APPS` uses `'blog.apps.BlogConfig'` to guarantee signal registration.
- **Safe Profile Access:**
	- In all views, `Profile.objects.get_or_create(user=user)` is used instead of `user.profile` to prevent `RelatedObjectDoesNotExist` errors.
	- A one-time script was run to create missing profiles for existing users.
- **Common Issue:**
	- If the signal is not registered or users were created before the signal, accessing `user.profile` will fail. Always use `get_or_create` for robustness.

---

## 2. Authentication, Navigation, and Security
- **Navigation Bar:**
	- The nav bar adapts to authentication state: shows Login/Register for anonymous users, Profile/Logout for authenticated users.
- **Logout Security:**
	- Logout is performed via a POST form, not a link, to prevent CSRF and accidental logouts. This fixes HTTP 405 errors.
	- The logout button is styled to look like a link for user experience.
- **Redirection:**
	- `LOGIN_REDIRECT_URL` and `LOGOUT_REDIRECT_URL` are set to `'/'` in `settings.py` to ensure users always return to the homepage after login/logout.

---

## 3. URL and Template Management
- **URL Names:**
	- All URLs are named and referenced consistently in templates (e.g., `'home'`, `'post_list'`).
	- The root URL (`''`) is mapped to the post list view and named `'home'` for easy redirects and navigation.
- **Template Structure:**
	- All templates extend `'blog/base.html'` for consistent layout and styling.
	- Static files (CSS) are loaded using `{% load static %}` and referenced with the correct path.
- **Template and URL Errors Fixed:**
	- `NoReverseMatch` errors were resolved by ensuring all URL names exist and are used correctly.
	- `TemplateDoesNotExist` errors were fixed by matching template paths to Django conventions (e.g., `blog/login.html`).

---

## 4. Database and Migration Issues
- **Missing Tables:**
	- `ProgrammingError: relation "blog_profile" does not exist` was fixed by running migrations after model changes.
- **Duplicate App Labels:**
	- `ImproperlyConfigured: Application labels aren't unique, duplicates: blog` was fixed by ensuring only one entry for the blog app in `INSTALLED_APPS` (preferably `'blog.apps.BlogConfig'`).

---

## 5. Styling and User Experience
- **Modern CSS:**
	- A custom stylesheet (`blog/static/blog/style.css`) was added for a clean, modern look.
	- The blog title, navigation, buttons, and forms are styled for clarity and usability.
- **Responsive Design:**
	- The layout is responsive and works well on both desktop and mobile.

---

## 6. Testing and Debugging
- **Manual Testing:**
	- Registration, login, logout, profile update, and all CRUD operations for posts were tested via the browser.
- **Automated Testing (optional):**
	- Example `curl` commands were provided for API-like testing of registration, login, and authenticated views, including CSRF handling.

---

## 7. Common Problems & Solutions
- **405 on /logout/**: Use a POST form for logout, not a link.
- **RelatedObjectDoesNotExist for profile**: Use `get_or_create` and ensure signals are registered.
- **NoReverseMatch**: Double-check all URL names in templates and views.
- **TemplateDoesNotExist**: Ensure template paths match what Django expects.
- **Duplicate app label**: Only one entry for the blog app in `INSTALLED_APPS`.
- **Missing tables**: Run migrations after model changes.

---

## 8. Best Practices
- Register signals in `apps.py` using `ready()`.
- Use `get_or_create` for all profile access.
- Use named URLs everywhere for maintainability.
- Always use CSRF protection in forms.
- Use POST for logout for security.
- Keep navigation adaptive to authentication state.
- Document all major changes and issues in this file for future reference.

---

## How to Test
1. Register a new user and ensure a profile is created.
2. Log in and out using the navigation (check POST logout works).
3. Access all CRUD views for posts.
4. Check navigation adapts to authentication state.
5. Try accessing `/logout/` via GET (should 405), and via the nav button (should work).
6. Try accessing the profile page for any user (should never error).

---
For more details, see code comments, previous commit messages, and this file.
