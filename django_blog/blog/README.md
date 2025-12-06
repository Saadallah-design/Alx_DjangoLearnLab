# Django Blog App Features

This Django blog app provides a full set of CRUD (Create, Read, Update, Delete) operations for blog posts, with user authentication and permissions.

## Features

### 1. List All Posts
- **URL:** `/` (home)
- **Description:** Displays all blog posts with titles, author, date, and a snippet of content.
- **Access:** Public (anyone can view).

### 2. View Post Details
- **URL:** `/post/<id>/`
- **Description:** Shows the full content of a single post, including author and date.
- **Access:** Public.

### 3. Create a New Post
- **URL:** `/post/new/`
- **Description:** Authenticated users can create a new post using a form.
- **Fields:** Title, Content (author is set automatically).
- **Access:** Only logged-in users.
- **Special Note:** Author is set to the currently logged-in user; not editable via the form.

### 4. Edit a Post
- **URL:** `/post/<id>/edit/`
- **Description:** Allows the post's author to edit the title and content.
- **Access:** Only the original author (must be logged in).
- **Special Note:** Other users cannot edit posts they do not own.

### 5. Delete a Post
- **URL:** `/post/<id>/delete/`
- **Description:** Allows the post's author to delete their post after confirmation.
- **Access:** Only the original author (must be logged in).

## Permissions & Data Handling
- Only authenticated users can create, edit, or delete posts.
- Users can only edit or delete their own posts.
- All forms use CSRF protection.
- Author field is set automatically in the backend for security.
- Posts are ordered by publication date (newest first).

## Templates
- `home.html`: List of all posts.
- `post_detail.html`: Full post view.
- `post_form.html`: Used for both create and edit.
- `post_confirm_delete.html`: Delete confirmation.

## Usage
1. Register or log in to create posts.
2. Use the navigation links to create, edit, or delete your posts.
3. Only your own posts can be edited or deleted.

For more details, see comments in `views.py` and the templates.
