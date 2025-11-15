# r4-prod

Production Docker stack for the **Re4ctoR SaaS API**.

This repository contains everything needed to run Re4ctoR as a small self-hosted SaaS node:

- `docker-compose.yml` – full stack (core, VRF, gateway, Caddy).
- `Caddyfile` – HTTPS reverse proxy configuration.
- `Dockerfile.core` – build file for the local/dev core API.
- `core_dev.py` – development version of the core API.
- `.env.example` – example environment variables for production.

## Local test

```bash
docker compose up -d
Then:

Core health: curl http://127.0.0.1:8080/health

Gateway health: curl http://127.0.0.1:8082/v1/health

VPS deployment (high level)
Create DNS A record: api.re4ctor.net -> <VPS IP>.

On the VPS:
git clone https://github.com/pipavlo82/r4-prod.git
cd r4-prod
cp .env.example .env
docker compose up -d

Caddy will automatically obtain a real TLS certificate for api.re4ctor.net.
