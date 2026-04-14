FROM nginx:1.26-alpine

RUN rm /etc/nginx/conf.d/default.conf

RUN mkdir -p /etc/nginx/certs

COPY nginx.conf /etc/nginx/nginx.conf
COPY index.html /usr/share/nginx/html/index.html
COPY certs/server.crt /etc/nginx/certs/server.crt
COPY certs/server.key /etc/nginx/certs/server.key

EXPOSE 8443

HEALTHCHECK --interval=30s --timeout=5s \
    CMD wget --no-check-certificate --spider -q https://127.0.0.1:8443 || exit 1