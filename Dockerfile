FROM python:3.12-alpine AS prepare

WORKDIR /work
COPY Caddyfile ./Caddyfile
COPY public ./public
COPY scripts ./scripts
RUN python scripts/apply_public_branding.py

FROM caddy:2-alpine

COPY --from=prepare /work/Caddyfile /etc/caddy/Caddyfile
COPY --from=prepare /work/public /srv

EXPOSE 8080

CMD ["caddy", "run", "--config", "/etc/caddy/Caddyfile", "--adapter", "caddyfile"]
