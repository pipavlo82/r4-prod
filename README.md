# ☢️ RE4CTOR — Production Stack (`r4-prod`)

Hardened Docker stack for running the **Re4ctoR entropy appliance & PQ-VRF gateway** as a small **self-hosted SaaS node**.

This repository is the “production wrapper” around the main project:

- Core project (design, proofs, SDKs):  
  👉 https://github.com/pipavlo82/r4-monorepo  

`r4-prod` gives you a reproducible way to run Re4ctoR on a VPS or bare-metal host with:

- Sealed entropy core (`re4_dump`)  
- VRF / PQ node  
- HTTPS gateway (Caddy reverse proxy)  
- Single `docker compose up -d` deployment

---

## 📦 What’s Inside

**Top-level layout (simplified):**

```text
r4-prod/
├── docker-compose.yml      # Full stack: core, vrf, gateway, Caddy
├── Caddyfile               # HTTPS reverse proxy (api.re4ctor.*)
├── core_dev.py             # Dev-only core API for local testing
├── Dockerfile.core         # Build file for local/dev core API
├── site/                   # Static landing page (Reactor-style)
│   └── index.html
├── .env.example            # Example production env configuration
└── README.md               # This file
Services (from docker-compose.yml):

r4-core

Port: 8080 (internal)

Role: sealed entropy appliance (/random)

r4-vrf

Port: 8081 (internal)

Role: VRF / PQ node (/random_dual, /vrf etc.)

r4-gateway

Port: 8082 (internal HTTP)

Role: public HTTP API (/v1/random, /v1/vrf, /v1/health)

caddy

Port: 80 / 443 (public)

Role: HTTPS reverse proxy → r4-gateway

Auto-TLS via Let’s Encrypt for api.re4ctor.*

🚀 Local Test (No TLS, Developer Mode)
This brings up the full stack on your local machine.

bash
Copy code
git clone https://github.com/pipavlo82/r4-prod.git
cd r4-prod

# For local tests you can usually skip .env, or copy it:
cp .env.example .env

docker compose up -d
Health checks
bash
Copy code
# Core entropy engine
curl http://127.0.0.1:8080/health

# VRF / PQ node
curl http://127.0.0.1:8081/health

# Public gateway (HTTP only, no TLS)
curl http://127.0.0.1:8082/v1/health
Get random bytes (dev)
bash
Copy code
curl -H "X-API-Key: demo" \
  "http://127.0.0.1:8082/v1/random?n=8&fmt=hex"
🌐 VPS Deployment (Production, HTTPS)
This is the typical path to run Re4ctoR as a small production-grade SaaS node.

Create DNS record

In your DNS provider:

Type: A

Name: api.re4ctor.com (or .net, .org, etc.)

Value: <VPS_IP> (public IP of your server)

Clone and configure on the VPS

bash
Copy code
ssh <user>@<VPS_IP>

git clone https://github.com/pipavlo82/r4-prod.git
cd r4-prod

cp .env.example .env
nano .env    # or any editor you prefer
Set essential variables in .env

The exact list is in .env.example. Typical fields:

DOMAIN=api.re4ctor.com

CADDY_EMAIL=you@example.com — email for Let’s Encrypt

R4_API_KEY=change-me — default API key for /v1/random etc.

R4_STRICT_FIPS=1 — optional, enables stricter FIPS-like behavior

Save the file when done.

Bring the stack up

bash
Copy code
docker compose up -d
Verify HTTPS

After Caddy obtains a certificate (usually 10–60 seconds):

bash
Copy code
# Health
curl https://api.re4ctor.com/v1/health

# Random values via gateway
curl -H "X-API-Key: change-me" \
  "https://api.re4ctor.com/v1/random?n=8&fmt=hex"
You should see hexadecimal random bytes and a 200 response.

🔧 Configuration Reference
Always treat .env as secret and never commit it to Git.

Key parameters (actual list in .env.example):

Variable	Description
DOMAIN	Public hostname to serve via HTTPS (e.g. api.re4ctor.com).
CADDY_EMAIL	Email used by Let’s Encrypt for issuing TLS certificates.
R4_API_KEY	Default API key required in X-API-Key header at the gateway.
R4_STRICT_FIPS	Optional flag (0/1) enabling stricter startup tests / fail-closed behavior.
R4_LOG_LEVEL	Log verbosity for API containers (info, debug, warning, …).
R4_CORE_IMAGE	(Optional) override for core Docker image tag.
R4_VRF_IMAGE	(Optional) override for VRF Docker image tag.

After any change to .env:

bash
Copy code
docker compose down
docker compose up -d
🌐 Public API Surface (Gateway)
Assuming production hostname https://api.re4ctor.com:

Health:

bash
Copy code
curl https://api.re4ctor.com/v1/health
Random words (32-bit):

bash
Copy code
curl -H "X-API-Key: <YOUR_API_KEY>" \
  "https://api.re4ctor.com/v1/random?n=8&fmt=hex"
VRF / signed randomness (ECDSA or dual-signed, depending on build):

bash
Copy code
curl -H "X-API-Key: <YOUR_API_KEY>" \
  "https://api.re4ctor.com/v1/vrf?sig=ecdsa"
Each call returns structured JSON with randomness, timestamp and signature metadata ready for on-chain verification (see main repo).

🔄 Updating & Maintenance
Pull latest images and restart
bash
Copy code
cd r4-prod
git pull
docker compose pull
docker compose up -d
Check logs
bash
Copy code
docker compose logs -f r4-core
docker compose logs -f r4-vrf
docker compose logs -f r4-gateway
docker compose logs -f caddy
Stop the stack
bash
Copy code
docker compose down
🛡️ Security Notes
Treat the VPS as part of your crypto perimeter:

Restrict SSH access (keys only, no password logins).

Keep the host OS and Docker engine updated.

Use a firewall / security group to expose only 80/443 externally.

Never expose core ports (8080, 8081, 8082) directly to the internet.
All external traffic must go through Caddy on 443.

Rotate R4_API_KEY regularly.
If rotating:

Update .env

Restart stack with docker compose up -d

For deeper threat model, entropy proofs and statistical test reports, see:
👉 https://github.com/pipavlo82/r4-monorepo

🔗 Related Repositories
Core project (design, code, proofs):
https://github.com/pipavlo82/r4-monorepo

SaaS API demo (reference implementation):
https://github.com/pipavlo82/r4-saas-api

📞 Contact
Maintainer: Pavlo Tvardovskyi

Email: shtomko@gmail.com

GitHub: https://github.com/pipavlo82

Re4ctoR — fairness you can prove. On-chain. Cryptographically.
