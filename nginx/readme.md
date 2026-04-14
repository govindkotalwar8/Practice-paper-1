## Host an nginx server to expose a simple html file over https on port 8443. Generate self signed certificates to support the TLS connection. Curl the page to validate the setup with and without the -k option. Use docker if needed.


## Generate Self-Signed TLS Certificates

```bash
mkdir certs

openssl req -x509 -nodes -days 365 \
-newkey rsa:2048 \
-keyout certs/server.key \
-out certs/server.crt \
-subj "/CN=localhost"
```

### Build Image

```bash
docker build -t my-nginx .
```

### Run Container

```bash
docker run -d --name nginx-server -p 8443:8443 my-nginx
```

### Validate

Without trusting cert:

```bash
curl https://localhost:8443
```

Error → self-signed certificate.

With `-k`:

```bash
curl -k https://localhost:8443
```

### Make it work **without `-k`**

Import certificate to system trust store.

**PowerShell (Admin):**

```powershell
Import-Certificate -FilePath .\server.crt -CertStoreLocation Cert:\LocalMachine\Root
```

### Validate again

```bash
curl https://localhost:8443
```
