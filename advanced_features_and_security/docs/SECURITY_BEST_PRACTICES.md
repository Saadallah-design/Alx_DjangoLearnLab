# Django Security Best Practices

This guide covers essential security settings and best practices for Django projects. Applying these will help protect your application from common web vulnerabilities and ensure safer deployments.

## Key Security Settings

### 1. SECURE_BROWSER_XSS_FILTER
- **Purpose:** Enables the browser's built-in XSS (Cross-Site Scripting) filter.
- **Setting:**
  ```python
  SECURE_BROWSER_XSS_FILTER = True
  ```
- **Effect:** Adds `X-XSS-Protection: 1; mode=block` header to responses.

### 2. X_FRAME_OPTIONS
- **Purpose:** Prevents your site from being embedded in an iframe (clickjacking protection).
- **Setting:**
  ```python
  X_FRAME_OPTIONS = 'DENY'  # or 'SAMEORIGIN'
  ```
- **Effect:** Adds `X-Frame-Options: DENY` header to responses.

### 3. SECURE_CONTENT_TYPE_NOSNIFF
- **Purpose:** Prevents browsers from guessing content types (MIME sniffing).
- **Setting:**
  ```python
  SECURE_CONTENT_TYPE_NOSNIFF = True
  ```
- **Effect:** Adds `X-Content-Type-Options: nosniff` header to responses.

### 4. CSRF_COOKIE_SECURE
- **Purpose:** Ensures CSRF cookies are only sent over HTTPS.
- **Setting:**
  ```python
  CSRF_COOKIE_SECURE = True
  ```
- **Effect:** CSRF cookie is marked as secure, reducing risk of interception.

### 5. SESSION_COOKIE_SECURE
- **Purpose:** Ensures session cookies are only sent over HTTPS.
- **Setting:**
  ```python
  SESSION_COOKIE_SECURE = True
  ```
- **Effect:** Session cookie is marked as secure, reducing risk of interception.

---

## Additional Best Practices

- **Use HTTPS:** Always deploy with HTTPS in production.
- **Keep Django & dependencies updated:** Regularly update to latest versions.
- **Set DEBUG = False in production:** Never run with `DEBUG = True` in production.
- **Use strong, unique SECRET_KEY:** Store securely, never commit to version control.
- **Restrict ALLOWED_HOSTS:** Set to your domain(s) only.
- **Validate user input:** Use Django forms and model validation.
- **Limit permissions:** Use Django's permission system and groups.
- **Regularly audit your code:** Check for vulnerabilities and sensitive data leaks.

---

## Example: Secure Settings in settings.py
```python
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']
```

---

## References
- [Django Security Documentation](https://docs.djangoproject.com/en/5.2/topics/security/)
- [OWASP Secure Headers Project](https://owasp.org/www-project-secure-headers/)
- [Mozilla Observatory](https://observatory.mozilla.org/)

---

**Always test your security settings in a staging environment before deploying to production!**
