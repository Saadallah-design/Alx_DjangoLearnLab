# Tagging and Search Features Usage Guide

## How to Add Tags to Posts
1. **Create or Edit a Post:**
   - When creating a new post or editing an existing one, you’ll see a field labeled "Tags" in the post form.
2. **Enter Tags:**
   - Type one or more tags separated by commas (e.g., `art, science, technology`).
   - You can add new tags or use existing ones; django-taggit will handle both.
3. **Save the Post:**
   - After saving, the tags will be associated with your post and displayed on the post detail page.

## How Tags Are Displayed
- On each post’s detail page, tags appear as clickable links.
- Clicking a tag will show all posts that share that tag.

## How to Use the Search Bar
1. **Locate the Search Bar:**
   - The search bar is available at the top of every page in the navigation area.
2. **Enter a Query:**
   - Type any keyword, post title, or tag name into the search bar.
   - The search is case-insensitive and ignores extra spaces.
3. **View Results:**
   - The search results page will display all posts where the query matches the post’s title, content, or any associated tag.
   - Each result shows the post title and its tags (with links to tag-filtered views).

## Example Usage
- **Adding Tags:**
  - Enter: `django, tutorial, beginner` in the tags field when creating a post.
- **Searching by Tag:**
  - Type `django` in the search bar to find all posts tagged with "django" or mentioning it in the title/content.
- **Searching by Title/Content:**
  - Type part of a post’s title or a keyword from its content to find relevant posts.

## Tips
- Use descriptive tags to make posts easier to find.
- You can combine tags and keywords in the search bar for broader results.
- Tags are managed automatically; no need to create them separately.