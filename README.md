# Wu Xing public page – Railway build v2

Public route:

- `/learn/wu-xing/`

Verification routes:

- `/health` must return `ok`
- `/version.txt` must show `WU_XING_PUBLIC_BUILD=wu-xing-2026-07-18-v2`

## Deploy

Push the files in this directory to the root of the GitHub branch connected to Railway. The repository root must contain `Dockerfile`, `Caddyfile`, `railway.json`, and `public/` directly.

Railway must deploy the commit containing this version. In the deployment build logs, confirm `Using detected Dockerfile!`. Remove any dashboard Start Command override so the Dockerfile CMD is used.

The route `/learn/wu-xing/` is served from `public/learn/wu-xing/index.html`. Replacing only the root `public/index.html` does not update this page.
