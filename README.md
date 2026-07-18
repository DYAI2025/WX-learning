# Wu Xing public Learn pages

## Public routes

- `/learn/wu-xing/` — Wu Xing foundation hub
- `/learn/wu-xing/tcm-organs/` — BZG-33 historical TCM-organ correspondence guide

## Verification routes

- `/health` must return `ok`
- `/version.txt` must contain both the Wu Xing hub build and `TCM_ORGANS_BUILD=wu-xing-tcm-organs-2026-07-19-v1`

## Build

The Docker prepare stage applies branding and authoritative links, validates the foundation page, then validates the BZG-33 page, source artifacts, claims matrix, SEO, structured data, accessibility structure and analytics hooks.

## Release boundary

The canonical identity is `https://sizhuatelier.shop/`. Railway URLs are operational verification targets only. A successful image build or merge does not prove that the canonical route is live.
