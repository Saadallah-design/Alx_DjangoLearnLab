# Deployment Configuration for HTTPS

To serve your Django application securely over HTTPS, you must configure your web server (e.g., Nginx or Apache) with SSL/TLS certificates.

## Nginx Example

1. **Obtain SSL Certificate**
   - Use Let's Encrypt (free) or purchase a certificate.
   - Example with Certbot:
     ```sh
     sudo apt install certbot python3-certbot-nginx
     sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
     ```

2. **Configure Nginx**
   - Edit your Nginx site config:
     ```nginx
     server {
         listen 443 ssl;
         server_name yourdomain.com www.yourdomain.com;

         ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
         ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
         include /etc/letsencrypt/options-ssl-nginx.conf;
         ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

         location / {
             proxy_pass http://127.0.0.1:8000;
             proxy_set_header Host $host;
             proxy_set_header X-Real-IP $remote_addr;
             proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
             proxy_set_header X-Forwarded-Proto $scheme;
         }
     }

     server {
         listen 80;
         server_name yourdomain.com www.yourdomain.com;
         return 301 https://$host$request_uri;
     }
     ```

## Apache Example

1. **Enable SSL Module**
   ```sh
   sudo a2enmod ssl
   sudo a2ensite default-ssl
   sudo systemctl reload apache2
   ```

2. **Configure Virtual Host**
   - Edit your Apache config:
     ```apache
     <VirtualHost *:443>
         ServerName yourdomain.com
         SSLEngine on
         SSLCertificateFile /etc/letsencrypt/live/yourdomain.com/fullchain.pem
         SSLCertificateKeyFile /etc/letsencrypt/live/yourdomain.com/privkey.pem
         # Proxy to Django
         ProxyPass / http://127.0.0.1:8000/
         ProxyPassReverse / http://127.0.0.1:8000/
     </VirtualHost>

     <VirtualHost *:80>
         ServerName yourdomain.com
         Redirect permanent / https://yourdomain.com/
     </VirtualHost>
     ```

## Notes
- Always test your SSL configuration.
- Use strong ciphers and protocols.
- Renew certificates regularly.
- For production, set Django's `ALLOWED_HOSTS` to your domain(s).

---

For more details, see [Mozilla SSL Configuration Generator](https://ssl-config.mozilla.org/) and [Let's Encrypt Documentation](https://letsencrypt.org/getting-started/).
