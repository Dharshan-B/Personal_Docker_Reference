# 🔒 Automated SSL Reverse Ingress (Nginx + Certbot Let's Encrypt)

A production-grade edge proxy designed to enforce HTTPS, terminate SSL encryption, and dynamically handle domain validation challenges for free Let's Encrypt renewals.

## ⚙️ How It Works
* **Nginx:** Public-facing proxy listening on ports `80` and `443`. It intercepts traffic and routes it internally.
* **Certbot (Let's Encrypt):** A container running a renewal loop. Every 12 hours, it checks if the SSL certificates are nearing expiration and contacts Let's Encrypt to renew them.
* **Shared Volumes:** Nginx and Certbot share the certificates volume (`cert-vol`) and challenge root folder (`web-root`).

## 🔄 Data Flow
1. Client hits Nginx on port `80` (HTTP). Nginx enforces a `301 Redirect` to port `443` (HTTPS).
2. Let's Encrypt challenges the ownership of the domain via the ACME HTTP-01 challenge.
3. Certbot writes the challenge file to the shared `/var/www/html` volume. Nginx serves it to Let's Encrypt verification bots.
4. Once verified, Certbot downloads the active SSL certificates into `/etc/letsencrypt/` (shared volume).
5. Nginx uses these certs to encrypt client traffic securely.

## 🛠️ Step-by-Step Commands

### ⚠️ Note on Domain Requirements
Let's Encrypt cannot issue SSL certificates for `localhost`. This setup requires a real, public domain pointed at your server's IP address.

### 1. Initial Configuration
Modify `nginx.conf` to replace `example.com` with your actual domain.

### 2. Start Nginx and Trigger Certbot Challenge
Run the stack in the background:
```bash
docker compose up -d
```

### 3. Generate Certificates
To trigger the certificate generation manually, run this command (replace with your domain and email):
```bash
docker compose run --rm certbot certonly --webroot --webroot-path=/var/www/html -d example.com -d www.example.com --email admin@example.com --agree-tos --no-eff-email
```

### 4. Enable SSL in Nginx
Once the certificates are generated inside `cert-vol`, open `nginx.conf`, uncomment the SSL block (lines 14–25), and reload Nginx:
```bash
docker compose exec nginx nginx -s reload
```

### 5. Clean Up
```bash
docker compose down -v
```
