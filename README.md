<div align="center">

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║      ██████╗ ███████╗██╗  ██╗ ██████╗████████╗ ██████╗ ██████╗             ║
║      ██╔══██╗██╔════╝██║  ██║██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗            ║
║      ██████╔╝█████╗  ███████║██║        ██║   ██║   ██║██████╔╝            ║
║      ██╔══██╗██╔══╝  ╚════██║██║        ██║   ██║   ██║██╔══██╗            ║
║      ██║  ██║███████╗     ██║╚██████╗   ██║   ╚██████╔╝██║  ██║            ║
║      ╚═╝  ╚═╝╚══════╝     ╚═╝ ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝            ║
║                                                                              ║
║           ⚡ HIGH-ASSURANCE CRYPTOGRAPHIC RANDOMNESS ⚡                      ║
║                                                                              ║
║              FIPS-Ready Entropy Appliance & PQ-VRF Gateway                  ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

[![FIPS 140-3](https://img.shields.io/badge/FIPS-140--3%20Ready-00bcd4?style=for-the-badge&logo=shield&logoColor=white)](https://github.com/pipavlo82/r4-monorepo)
[![ML-DSA-65](https://img.shields.io/badge/PQ-ML--DSA--65-9acd32?style=for-the-badge&logo=quantum&logoColor=white)](https://github.com/pipavlo82/r4-monorepo)
[![BigCrush](https://img.shields.io/badge/Validated-BigCrush%20%2B%20NIST-ff8c3c?style=for-the-badge&logo=test&logoColor=white)](https://github.com/pipavlo82/r4-monorepo)
[![License](https://img.shields.io/badge/License-Proprietary-d4af37?style=for-the-badge)](./LICENSE)

</div>

---

## 📡 Overview

**Re4ctoR** is a production-grade **cryptographic randomness reactor** — a sealed entropy appliance with dual-signed VRF outputs **(ECDSA + ML-DSA-65)** engineered for:

- 🔗 **Blockchain consensus** & L2 sequencers
- 🎮 **Fair gaming** & NFT raffles  
- 🏦 **Financial systems** under regulatory scrutiny
- 🛡️ **Mission-critical infrastructure** requiring provable fairness

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│           ⚛️  SEALED ENTROPY CORE (re4_dump)                       │
│                         │                                           │
│                         │ < 1ms latency                             │
│                         ▼                                           │
│           ┌─────────────────────────┐                              │
│           │   VRF / PQ Signature    │  ◄── ECDSA + ML-DSA-65       │
│           │   (Dual-Signed Output)  │                              │
│           └─────────────────────────┘                              │
│                         │                                           │
│                         ▼                                           │
│           ╔═════════════════════════╗                              │
│           ║   HTTPS Gateway (API)   ║  ◄── /v1/random, /v1/vrf     │
│           ╚═════════════════════════╝                              │
│                         │                                           │
│                         ▼                                           │
│                   🌐 Public API                                     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## ⚡ Quick Start

### 🔧 Local Development (HTTP, No TLS)

```bash
# Clone the repository
git clone https://github.com/pipavlo82/r4-prod.git
cd r4-prod

# Copy environment template
cp .env.example .env

# Start the stack
docker compose up -d

# Health check
curl http://127.0.0.1:8082/v1/health

# Get random bytes
curl -H "X-API-Key: demo" \
  "http://127.0.0.1:8082/v1/random?n=8&fmt=hex"
```

### 🌐 Production Deployment (VPS + HTTPS)

```bash
# 1. Configure DNS
# Create A record: api.re4ctor.com → <YOUR_VPS_IP>

# 2. SSH to VPS and clone
ssh user@your-vps-ip
git clone https://github.com/pipavlo82/r4-prod.git
cd r4-prod

# 3. Configure environment
cp .env.example .env
nano .env  # Set DOMAIN, CADDY_EMAIL, R4_API_KEY

# 4. Deploy
docker compose up -d

# 5. Verify HTTPS
curl https://api.re4ctor.com/v1/health
curl -H "X-API-Key: your-key" \
  "https://api.re4ctor.com/v1/random?n=8&fmt=hex"
```

---

## 🏗️ Architecture

```
┌───────────────────────────────────────────────────────────────────┐
│                         DOCKER STACK                              │
├───────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │  r4-core    │───▶│   r4-vrf    │───▶│ r4-gateway  │         │
│  │   :8080     │    │   :8081     │    │   :8082     │         │
│  │             │    │             │    │             │         │
│  │  Entropy    │    │  VRF + PQ   │    │  Public API │         │
│  │  Engine     │    │  Signatures │    │  Endpoints  │         │
│  └─────────────┘    └─────────────┘    └─────────────┘         │
│         │                   │                   │                │
│         └───────────────────┴───────────────────┘                │
│                             ▼                                    │
│                    ┌─────────────────┐                          │
│                    │     Caddy       │  ◄─── Let's Encrypt      │
│                    │  :80 / :443     │       Auto-TLS           │
│                    │                 │                          │
│                    │  HTTPS Proxy    │                          │
│                    └─────────────────┘                          │
│                             │                                    │
└─────────────────────────────┼────────────────────────────────────┘
                              ▼
                         🌍 Internet
                    (api.re4ctor.com)
```

### 📦 Container Roles

| Service | Port | Function |
|---------|------|----------|
| **r4-core** | 8080 | Sealed entropy appliance (`/random`) |
| **r4-vrf** | 8081 | VRF node with PQ signatures (`/random_dual`, `/vrf`) |
| **r4-gateway** | 8082 | Public HTTP API gateway (`/v1/*`) |
| **caddy** | 80/443 | HTTPS reverse proxy with auto-TLS |

---

## 🎯 Core Features

<table>
<tr>
<td width="50%" valign="top">

### 🔬 Statistical Validation
- ✅ **TestU01 BigCrush** passed
- ✅ **Dieharder** suite validated  
- ✅ **NIST SP 800-22** compliant
- ✅ **PractRand** multi-GB runs

Complete reports available for compliance audits.

</td>
<td width="50%" valign="top">

### 🛡️ FIPS Architecture
- ✅ **FIPS 140-3** design principles
- ✅ **FIPS 204 (ML-DSA-65)** aligned
- ✅ Documented KATs & entropy measurements
- ✅ Ready for lab submission

</td>
</tr>
<tr>
<td width="50%" valign="top">

### ⚛️ Post-Quantum VRF
- ✅ **Dual-signature** scheme:
  - `ECDSA(secp256k1)` — smart contract compatible
  - `ML-DSA-65` — quantum-resistant
- ✅ No redesign needed for PQ upgrade
- ✅ Open-source Solidity verifiers

</td>
<td width="50%" valign="top">

### 🔒 Sealed Entropy Core
- ✅ Signed binary with **fail-closed** mode
- ✅ Continuous self-tests
- ✅ Output halts on entropy degradation
- ✅ No silent fallback to weak randomness

</td>
</tr>
</table>

---

## 📊 Performance Metrics

```
┌──────────────────────┬─────────────────────────────────────────┐
│      METRIC          │              VALUE                      │
├──────────────────────┼─────────────────────────────────────────┤
│  ⚡ Latency          │  < 1 ms  (core → gateway, single hop)  │
│  🔬 Quality          │  NIST SP 800-22, Dieharder, BigCrush   │
│  🛡️ PQ Signatures    │  ECDSA + ML-DSA-65 (FIPS 204)          │
│  🔐 Security Model   │  HSM-grade, sealed core                 │
│  📈 Throughput       │  100k+ requests/day (Pro tier)          │
│  🌐 Multi-region     │  Available in Enterprise plan           │
└──────────────────────┴─────────────────────────────────────────┘
```

---

## 🌍 API Reference

### Base URL
```
Production: https://api.re4ctor.com
Local Dev:  http://127.0.0.1:8082
```

### Authentication
All requests require `X-API-Key` header:
```bash
curl -H "X-API-Key: your-api-key" \
  "https://api.re4ctor.com/v1/random?n=8"
```

### Endpoints

#### `GET /v1/health`
Health check endpoint (no auth required)

```bash
curl https://api.re4ctor.com/v1/health
```

**Response:**
```json
{
  "status": "ok",
  "timestamp": "2025-01-15T10:30:00Z",
  "version": "1.0.0"
}
```

---

#### `GET /v1/random`
Generate cryptographically secure random values

**Parameters:**
- `n` (required): Number of 32-bit words (1-256)
- `fmt` (optional): Output format — `hex`, `base64`, `int` (default: `hex`)

**Example:**
```bash
curl -H "X-API-Key: demo" \
  "https://api.re4ctor.com/v1/random?n=8&fmt=hex"
```

**Response:**
```json
{
  "words": [
    "0x8f3a2b1c",
    "0x4e7d9a2f",
    "0xb5c8e1d6",
    "0x7a9f3e4b",
    "0xc2d5f8a9",
    "0x6b4e3c1f",
    "0x9a7d2e5c",
    "0x3f8b1d6a"
  ],
  "format": "hex",
  "timestamp": "2025-01-15T10:30:00Z"
}
```

---

#### `GET /v1/vrf`
Verifiable Random Function with cryptographic signatures

**Parameters:**
- `sig` (optional): Signature scheme — `ecdsa`, `ml-dsa-65`, `dual` (default: `ecdsa`)

**Example:**
```bash
curl -H "X-API-Key: demo" \
  "https://api.re4ctor.com/v1/vrf?sig=dual"
```

**Response:**
```json
{
  "value": "0xa7b3c9d2e5f18a4c",
  "timestamp": "2025-01-15T10:30:00Z",
  "signatures": {
    "ecdsa": {
      "r": "0x3045022100...",
      "s": "0x02204f8e...",
      "v": 27
    },
    "ml_dsa_65": {
      "signature": "0x7f8e9d3c...",
      "public_key": "0xa1b2c3d4..."
    }
  },
  "verification": {
    "ecdsa_verified": true,
    "ml_dsa_65_verified": true
  }
}
```

---

## 💰 Pricing Tiers

<table>
<tr>
<th>Plan</th>
<th>Price</th>
<th>Features</th>
<th>Best For</th>
</tr>
<tr>
<td><strong>🆓 Dev / Free</strong></td>
<td><strong>$0/mo</strong></td>
<td>
• 1,000 requests/day<br>
• Shared gateway<br>
• Basic endpoints<br>
• 7-day logs
</td>
<td>Prototypes, CI/CD, Testing</td>
</tr>
<tr>
<td><strong>⚡ Pro / Scale</strong></td>
<td><strong>Custom</strong></td>
<td>
• 100k+ requests/day<br>
• SLA &lt; 10ms<br>
• Multi-region endpoints<br>
• Priority support<br>
• Quality reports
</td>
<td>Gaming, DeFi, NFT platforms</td>
</tr>
<tr>
<td><strong>🏢 Enterprise</strong></td>
<td><strong>Custom</strong></td>
<td>
• Dedicated VPC/on-prem<br>
• Full FIPS compliance<br>
• ML-DSA-65 PQ signatures<br>
• HSM integration<br>
• Contractual SLAs
</td>
<td>Banks, L2s, Regulated systems</td>
</tr>
</table>

---

## 🎮 Use Cases

### ⛓️ Blockchain & L2 Sequencers
```
┌─────────────────────────────────────────────────────────────┐
│  Use Case:  Validator rotation, staking lotteries          │
│  Solution:  Dual-signed VRF outputs verified on-chain      │
│  Benefits:  Provable fairness, no central authority        │
└─────────────────────────────────────────────────────────────┘
```

**Example: Solidity Integration**
```solidity
// Verify Re4ctoR VRF output on-chain
function verifyRandomness(
    bytes32 vrfOutput,
    bytes memory ecdsaSig,
    bytes memory mlDsaSig
) public view returns (bool) {
    // ECDSA verification (current contracts)
    bool ecdsaValid = verifyECDSA(vrfOutput, ecdsaSig);
    
    // ML-DSA-65 verification (quantum-resistant)
    bool mlDsaValid = verifyMLDSA(vrfOutput, mlDsaSig);
    
    return ecdsaValid && mlDsaValid;
}
```

---

### 🎮 Gaming & NFT Raffles
```
┌─────────────────────────────────────────────────────────────┐
│  Use Case:  Fair loot drops, raffle draws                  │
│  Solution:  Signed randomness + audit logs                 │
│  Benefits:  Mathematically provable fairness               │
└─────────────────────────────────────────────────────────────┘
```

---

### 🏦 Financial & Government Systems
```
┌─────────────────────────────────────────────────────────────┐
│  Use Case:  Regulatory compliance, auditable systems       │
│  Solution:  Complete artefact set (KAT, reports, docs)     │
│  Benefits:  FIPS 140-3 aligned, audit-ready                │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 Configuration

### Environment Variables

Create `.env` from `.env.example`:

```bash
cp .env.example .env
```

**Key variables:**

| Variable | Description | Example |
|----------|-------------|---------|
| `DOMAIN` | Public hostname for HTTPS | `api.re4ctor.com` |
| `CADDY_EMAIL` | Let's Encrypt email | `you@example.com` |
| `R4_API_KEY` | API authentication key | `your-secret-key-here` |
| `R4_STRICT_FIPS` | Enable strict FIPS mode (0/1) | `1` |
| `R4_LOG_LEVEL` | Logging verbosity | `info` |

**⚠️ Security:** Never commit `.env` to version control!

---

## 🛡️ Security Best Practices

### VPS Hardening
```bash
# 1. SSH key-only authentication
sudo nano /etc/ssh/sshd_config
# Set: PasswordAuthentication no

# 2. Firewall configuration
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS
sudo ufw enable

# 3. Fail2ban for SSH protection
sudo apt install fail2ban
```

### Docker Security
```bash
# Run containers as non-root user
# (Already configured in docker-compose.yml)

# Regular updates
docker compose pull
docker compose up -d

# Monitor logs
docker compose logs -f
```

### API Key Rotation
```bash
# 1. Generate new key
openssl rand -hex 32

# 2. Update .env
nano .env  # Set new R4_API_KEY

# 3. Restart services
docker compose restart
```

---

## 📚 Documentation & Artifacts

### Available Resources

```
📁 Transparency Bundle
├── 📄 AUDIT.md              # Architecture & threat model
├── 📊 BENCHMARKS.md         # Performance metrics
├── 🔬 NIST-STS-Report.pdf   # Statistical validation
├── 🧪 BigCrush-Results.txt  # TestU01 output
├── 🔐 KAT-Vectors.json      # Known Answer Tests
└── 📦 SBOM.json             # Software Bill of Materials
```

### Access Documentation

- **Core Project:** [r4-monorepo](https://github.com/pipavlo82/r4-monorepo)
- **API Reference:** [r4-saas-api](https://github.com/pipavlo82/r4-saas-api)
- **Integration Guides:** See `/docs` folder

---

## 🔄 Maintenance & Updates

### Check Service Health
```bash
# View all container status
docker compose ps

# Check individual logs
docker compose logs -f r4-core
docker compose logs -f r4-vrf
docker compose logs -f r4-gateway
docker compose logs -f caddy
```

### Update Stack
```bash
# Pull latest changes
git pull origin main

# Pull new images
docker compose pull

# Restart services
docker compose up -d

# Clean old images
docker image prune -a
```

### Backup Configuration
```bash
# Backup environment
cp .env .env.backup

# Backup Caddy data (TLS certificates)
docker compose exec caddy tar czf - /data > caddy-backup.tar.gz
```

---

## 📞 Support & Community

<div align="center">

### 🤝 Get Help

[![GitHub Issues](https://img.shields.io/github/issues/pipavlo82/r4-prod?style=for-the-badge)](https://github.com/pipavlo82/r4-prod/issues)
[![Email](https://img.shields.io/badge/Email-shtomko%40gmail.com-00bcd4?style=for-the-badge&logo=gmail)](mailto:shtomko@gmail.com)
[![GitHub](https://img.shields.io/badge/GitHub-pipavlo82-181717?style=for-the-badge&logo=github)](https://github.com/pipavlo82)

</div>

### 🐛 Report Issues
Found a bug? [Open an issue](https://github.com/pipavlo82/r4-prod/issues/new)

### 💡 Feature Requests
Have an idea? [Start a discussion](https://github.com/pipavlo82/r4-prod/discussions)

### 📧 Contact
- **Maintainer:** Pavlo Tvardovskyi
- **Email:** shtomko@gmail.com
- **GitHub:** [@pipavlo82](https://github.com/pipavlo82)

---

## 🗺️ Related Projects

| Project | Description | Link |
|---------|-------------|------|
| 🏗️ **r4-monorepo** | Core design, proofs, SDKs | [View →](https://github.com/pipavlo82/r4-monorepo) |
| 🌐 **r4-saas-api** | SaaS API reference implementation | [View →](https://github.com/pipavlo82/r4-saas-api) |
| 🔧 **r4-prod** | Production Docker stack | *You are here* |

---

## 📜 License

**Proprietary** — See [LICENSE](./LICENSE) file for details.

For commercial licensing inquiries: shtomko@gmail.com

---

<div align="center">

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│                 ⚛️  RE4CTOR — ENTROPY REACTOR                  │
│                                                                 │
│            Fairness you can prove. Cryptographically.          │
│                         On-chain.                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**⭐ Star this repo if you find it useful!**

[![GitHub stars](https://img.shields.io/github/stars/pipavlo82/r4-prod?style=social)](https://github.com/pipavlo82/r4-prod/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/pipavlo82/r4-prod?style=social)](https://github.com/pipavlo82/r4-prod/network/members)
[![GitHub watchers](https://img.shields.io/github/watchers/pipavlo82/r4-prod?style=social)](https://github.com/pipavlo82/r4-prod/watchers)

</div>

---

<div align="center">
<sub>Built with ⚡ by <a href="https://github.com/pipavlo82">Pavlo Tvardovskyi</a></sub>
</div>
