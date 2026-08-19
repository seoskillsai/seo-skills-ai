# Security Policy: SEO Skills AI

Security and data privacy are core architectural priorities for SEO Skills AI.

---

## 🛡️ Security Guarantees

1. **SSRF & Network Boundary Protection:**
   - All HTTP requests pass through `scripts/url_safety.py` to block SSRF, loopback attacks, private RFC1918 subnets, and AWS/Cloud metadata endpoints (`169.254.169.254`).
2. **Local Zero-Telemetry Execution:**
   - All audits run locally on your machine. No telemetry, user metrics, or target URLs are transmitted to any external third-party server.
3. **Isolated Credential Storage:**
   - Optional API credentials reside in `~/.config/seoskillsai/` with `0o600` permissions and are never checked into Git.

---

## 🚨 Reporting a Vulnerability

Please report security issues directly to security@seoskillsai.com with reproducible steps.
