# E-Commerce Product Schema & Google Merchant Center Guidelines

Specifications for structured shopping data and AI-generated image compliance.

---

## 🛒 1. Mandatory Product Schema Graph

All e-commerce product pages must implement:
- **`Product` / `ProductGroup`**: With `name`, `image`, `description`, `sku`, `gtin13` or `mpn`.
- **`offers` (Offer)**: `price`, `priceCurrency`, `availability` (`https://schema.org/InStock`), `priceValidUntil`.
- **`hasMerchantReturnPolicy`**: Direct link to return window, restocking fees, and return method.
- **`shippingDetails`**: Rate rules, handling time, and transit time by country destination.

---

## 📸 2. AI Product Image Disclosures

Per Google Merchant Center 2025/2026 policies:
- AI-generated product visual assets must include IPTC metadata tag `TrainedAlgorithmicMedia`.
