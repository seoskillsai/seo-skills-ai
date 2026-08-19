# Active 2026 Schema.org Types & Implementation Catalog

Complete reference for active, non-deprecated Schema.org types recognized by Google, Bing, and AI search engines.

---

## 📋 Active Supported Schemas

| Schema.org Type | Primary Use Case | Required / Recommended Fields |
| :--- | :--- | :--- |
| **`TechArticle`** | Technical guides, API documentation, skill specifications | `headline`, `author`, `datePublished`, `dateModified`, `isPartOf` |
| **`SoftwareApplication`** | CLI tools, web apps, AI agents, developer packages | `name`, `applicationCategory`, `operatingSystem`, `offers` |
| **`SoftwareSourceCode`** | Code snippets, repositories, CLI scripts | `programmingLanguage`, `codeRepository`, `runtimePlatform` |
| **`BreadcrumbList`** | Hierarchical navigation paths | `itemListElement`, `position`, `name`, `item` |
| **`Organization`** | Brand identity and knowledge graph anchoring | `name`, `url`, `logo`, `sameAs` |
| **`WebSite`** | Root domain entity | `name`, `url`, `publisher`, `potentialAction` |
| **`Product`** | E-commerce items, SaaS pricing tiers | `name`, `image`, `description`, `sku`, `offers` |
| **`LocalBusiness`** | Physical locations, agencies, multi-location branches | `name`, `address`, `geo`, `telephone`, `openingHoursSpecification` |
| **`DefinedTermSet`** | Glossaries, taxonomy definitions, SEO directories | `name`, `hasDefinedTerm` |
