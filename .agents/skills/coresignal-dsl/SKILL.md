---
name: coresignal-dsl
description: Use when working with Coresignal API, constructing Elasticsearch DSL queries, or referencing Coresignal schemas from docs/coresignal/.
---

# Coresignal Schema & DSL References

When constructing Elasticsearch DSL queries or inspecting available fields for Coresignal, refer directly to the schema definitions in `docs/coresignal/Employee APIs/`:

- **Multi-source Employee API**: `docs/coresignal/Employee APIs/Multi-source Employee API.json`
- **Clean Employee API**: `docs/coresignal/Employee APIs/Clean Employee API.json`
- **Base Employee API**: `docs/coresignal/Employee APIs/Base Employee API.json`
- **Employee Posts API**: `docs/coresignal/Employee APIs/Employee Posts API.json`

## Guidelines
1. **Always inspect the relevant schema JSON** above to verify:
   - Field names and exact spelling
   - Field types (`text`, `keyword`, `long`, `date`, `nested`)
   - Subfields (e.g. `.exact` for exact term matches on text fields)
   - Nested paths (e.g. `experience.*`, `education.*`, `skills.*`) requiring Elasticsearch `nested` query blocks.
2. Query endpoint: `POST https://api.coresignal.com/cdapi/v2/employee_multi_source/search/es_dsl` (or the respective API route).
