# Never Trust User Input: Examples & Cases

Trusting user input is one of the most common sources of security vulnerabilities in web applications. Attackers can exploit any unvalidated or unsanitized input to compromise your system, steal data, or disrupt service.

---

## Why Never Trust User Input?
- Users (or attackers) can send any data, not just what your form or UI expects.
- Browsers, proxies, and tools like curl or Postman can craft malicious requests.
- Even hidden fields, cookies, and headers can be manipulated.

---

## Common Attack Vectors

### 1. SQL Injection
**Vulnerable:**
```python
# BAD: Directly using user input in SQL
cursor.execute(f"SELECT * FROM users WHERE username = '{request.GET['username']}'")
```
**Safe:**
```python
# GOOD: Use parameterized queries
cursor.execute("SELECT * FROM users WHERE username = %s", [request.GET['username']])
```

### 2. Cross-Site Scripting (XSS)
**Vulnerable:**
```html
<!-- BAD: Rendering user input without escaping -->
<p>{{ user_input|safe }}</p>
```
**Safe:**
```html
<!-- GOOD: Default Django escaping -->
<p>{{ user_input }}</p>
```

### 3. Command Injection
**Vulnerable:**
```python
# BAD: Passing user input to shell commands
os.system(f"rm -rf {request.POST['folder']}")
```
**Safe:**
```python
# GOOD: Validate and sanitize input, avoid shell when possible
import shutil
folder = os.path.basename(request.POST['folder'])
shutil.rmtree(f"/safe/path/{folder}")
```

### 4. Path Traversal
**Vulnerable:**
```python
# BAD: Using user input in file paths
with open(f"/uploads/{request.GET['file']}") as f:
    data = f.read()
```
**Safe:**
```python
# GOOD: Restrict to allowed files only
allowed_files = {'report.pdf', 'summary.txt'}
filename = request.GET['file']
if filename in allowed_files:
    with open(f"/uploads/{filename}") as f:
        data = f.read()
```

### 5. Mass Assignment
**Vulnerable:**
```python
# BAD: Saving all POST data directly to a model
Book.objects.create(**request.POST)
```
**Safe:**
```python
# GOOD: Use forms or specify fields
form = BookForm(request.POST)
if form.is_valid():
    form.save()
```

---

## General Rules
- **Always validate and clean input:** Use Django forms, serializers, or custom validation.
- **Escape output:** Let Django auto-escape HTML in templates.
- **Whitelist allowed values:** Never trust that a value is safe just because it comes from your UI.
- **Never use user input in system commands, file paths, or SQL without validation.**

---

## References
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Django Security Guide](https://docs.djangoproject.com/en/5.2/topics/security/)

---

**Summary:**
- Attackers can manipulate any input field, header, cookie, or parameter.
- Always treat all user input as untrusted and dangerous until validated and sanitized.
- Use Django’s built-in tools to protect your app.
