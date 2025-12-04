# Understanding SECURE_PROXY_SSL_HEADER in Django

## What is SECURE_PROXY_SSL_HEADER?
`SECURE_PROXY_SSL_HEADER` is a Django setting that helps your application correctly detect secure (HTTPS) requests when running behind a proxy or load balancer (like Nginx, Apache, or Heroku).

## Why is it Needed?
- Many production deployments use a proxy to terminate SSL/TLS (handle HTTPS) and forward requests to Django over HTTP.
- The proxy adds a header (usually `X-Forwarded-Proto`) to tell Django whether the original request was HTTPS.
- Without this setting, Django may think requests are insecure and not enforce security features like HTTPS redirects, secure cookies, or HSTS.

## How Does it Work?
- You set:
  ```python
  SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
  ```
- Django checks the `HTTP_X_FORWARDED_PROTO` header in each request.
- If the header value is `'https'`, Django treats the request as secure.

## When Should You Use It?
- Use this setting if:
  - You deploy Django behind a proxy or load balancer that terminates SSL.
  - Your proxy sets the `X-Forwarded-Proto` header.
- Do **not** use it if you serve Django directly over HTTPS without a proxy.

## Example: Nginx Configuration
Nginx can be configured to set this header:
```nginx
proxy_set_header X-Forwarded-Proto $scheme;
```

## Security Implications
- Only trust this header if your proxy is secure and you control it.
- If an attacker can set this header, they could trick Django into treating insecure requests as secure.
- Always restrict direct access to your Django app from the internet; only allow traffic through your proxy.

## Summary
- `SECURE_PROXY_SSL_HEADER` ensures Django enforces HTTPS security features when behind a proxy.
- It is essential for correct security behavior in many production deployments.
- Always review your proxy and Django settings together for best security.

---

**References:**
- [Django Docs: SECURE_PROXY_SSL_HEADER](https://docs.djangoproject.com/en/5.2/ref/settings/#secure-proxy-ssl-header)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/)
