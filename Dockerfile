FROM python:3.12-alpine AS prepare

WORKDIR /work
COPY Caddyfile ./Caddyfile
COPY public ./public
COPY scripts ./scripts
COPY config ./config
RUN python scripts/apply_public_branding.py \
 && python scripts/apply_cornerstone_links.py \
 && python scripts/validate_public_content.py

FROM caddy:2-alpine

COPY --from=prepare /work/Caddyfile /etc/caddy/Caddyfile
COPY --from=prepare /work/public /srv

EXPOSE 8080

CMD ["caddy", "run", "--config", "/etc/caddy/Caddyfile", "--adapter", "caddyfile"]
