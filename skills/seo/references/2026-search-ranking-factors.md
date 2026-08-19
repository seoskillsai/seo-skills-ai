# 2026 Google Search Ranking Factors & Algorithmic Heuristics

This reference synthesizes primary-source search patents, Google Search Essentials, and empirical ranking benchmarks.

---

## 1. Primary Algorithmic Vectors

1. **Information Gain (Patent US 11,562,019 B2):**
   - Evaluates whether a source provides net-new data, original empirical testing, unique attributes, or proprietary benchmarks beyond the existing SERP cluster consensus.
2. **Interaction to Next Paint (INP):**
   - Core Web Vital evaluating main thread responsiveness to user input (clicks, keypresses, taps). Target: $< 200\text{ ms}$ at the 75th percentile of real users.
3. **Largest Contentful Paint (LCP):**
   - Render timing of the primary viewport centerpiece element. Target: $< 2.5\text{ s}$.
4. **Cumulative Layout Shift (CLS):**
   - Visual stability of the layout during rendering. Target: $< 0.1$.
5. **Entity-Attribute-Value (EAV) Knowledge Graph Grounding:**
   - Evaluates topical authority by calculating entity density and attribute relationships against Wikidata / Knowledge Graph triplets.
6. **Passage-Level Answer Citability (GEO):**
   - Direct 130–170 word self-contained semantic blocks answering specific search intents, favored by Google AI Overviews and LLM retrieval engines.
