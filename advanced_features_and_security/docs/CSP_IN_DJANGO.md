# Content Security Policy (CSP) in Django

A Content Security Policy (CSP) helps prevent XSS and other code injection attacks by specifying which sources of content are allowed to be loaded by browsers. You can enforce CSP in Django using the `django-csp` middleware or by manually setting the CSP header in your views.

---

## 1. Using django-csp Middleware

### Installation
```sh
pip install django-csp
```

### Configuration
Add `'csp'` to your `INSTALLED_APPS` and add `csp.middleware.CSPMiddleware` to your `MIDDLEWARE` list in `settings.py`:
```python
INSTALLED_APPS = [
    # ...
    'csp',
]

MIDDLEWARE = [
    # ...
    'csp.middleware.CSPMiddleware',
]

CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'", 'cdn.jsdelivr.net')
CSP_STYLE_SRC = ("'self'", 'fonts.googleapis.com')
CSP_FONT_SRC = ("'self'", 'fonts.gstatic.com')
```
- You can set more directives as needed (see django-csp docs).
- The middleware will automatically add the `Content-Security-Policy` header to all responses.

---

## 2. Manually Setting the CSP Header

You can also set the CSP header directly in your views or middleware:

### Example: In a View
```python
from django.http import HttpResponse

def my_view(request):
    response = HttpResponse("Hello, world!")
    response["Content-Security-Policy"] = "default-src 'self'; script-src 'self' cdn.jsdelivr.net; style-src 'self' fonts.googleapis.com; font-src 'self' fonts.gstatic.com"
    return response
```

### Example: Custom Middleware
```python
class CustomCSPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        response = self.get_response(request)
        response["Content-Security-Policy"] = "default-src 'self'"
        return response
```
Add your middleware to `MIDDLEWARE` in `settings.py`.

---

## References
- [django-csp documentation](https://github.com/mozilla/django-csp)
- [MDN: Content Security Policy (CSP)](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)

---

**Summary:**
- Use `django-csp` for easy, robust CSP enforcement.
- Or set the `Content-Security-Policy` header manually in views/middleware.
- Always test your CSP settings to avoid breaking legitimate scripts/styles.
