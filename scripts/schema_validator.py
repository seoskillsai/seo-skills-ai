#!/usr/bin/env python3
"""
SEO Skills AI — Enterprise 2026 Schema.org JSON-LD Deep Validator
Validates JSON-LD structures, required property graphs, and strictly flags deprecated Google schema types.
"""
import os
import sys
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

DEPRECATED_TYPES = {
    "HowTo": "Google removed HowTo rich results globally in September 2023.",
    "SpecialAnnouncement": "Google deprecated SpecialAnnouncement in July 2025.",
    "ClaimReview": "Google retired ClaimReview rich results in June 2025.",
    "VehicleListing": "Deprecated in June 2025.",
    "EstimatedSalary": "Deprecated in June 2025.",
    "LearningVideo": "Deprecated in June 2025.",
    "CourseInfo": "CourseInfo carousel retired June 2025."
}

REQUIRED_PROPERTIES = {
    "Article": ["headline", "author", "datePublished"],
    "TechArticle": ["headline", "author", "datePublished"],
    "SoftwareApplication": ["name", "applicationCategory"],
    "BreadcrumbList": ["itemListElement"],
    "Organization": ["name", "url"],
    "WebSite": ["name", "url"],
    "FAQPage": ["mainEntity"],
    "Product": ["name", "offers"]
}

def validate_schema_json(raw_json: str) -> dict:
    results = {
        "valid_json": False,
        "types_found": [],
        "deprecated_warnings": [],
        "missing_property_warnings": [],
        "has_graph": False,
        "entities_count": 0,
        "errors": []
    }

    try:
        data = json.loads(raw_json.strip())
        results["valid_json"] = True
    except Exception as e:
        results["errors"].append(f"JSON Parse Error: {e}")
        return results

    def inspect_entity(entity):
        if not isinstance(entity, dict):
            return
        etype = entity.get("@type")
        if etype:
            types = etype if isinstance(etype, list) else [etype]
            for t in types:
                results["types_found"].append(t)
                # Check deprecation
                if t in DEPRECATED_TYPES:
                    results["deprecated_warnings"].append(
                        f"Deprecated Schema Detected: '@type: {t}' — {DEPRECATED_TYPES[t]}"
                    )
                # Check required properties
                if t in REQUIRED_PROPERTIES:
                    for req_prop in REQUIRED_PROPERTIES[t]:
                        if req_prop not in entity:
                            results["missing_property_warnings"].append(
                                f"Schema '@type: {t}' missing recommended property '{req_prop}'"
                            )
            results["entities_count"] += 1

        for k, v in entity.items():
            if isinstance(v, dict):
                inspect_entity(v)
            elif isinstance(v, list):
                for item in v:
                    if isinstance(item, dict):
                        inspect_entity(item)

    if isinstance(data, dict):
        if "@graph" in data and isinstance(data["@graph"], list):
            results["has_graph"] = True
            for item in data["@graph"]:
                inspect_entity(item)
        else:
            inspect_entity(data)
    elif isinstance(data, list):
        for item in data:
            inspect_entity(item)

    return results

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python schema_validator.py <json_string_or_file>")
        sys.exit(1)
    arg = sys.argv[1]
    if arg.endswith(".json"):
        from scripts.path_safety import resolve_workspace_path
        path = resolve_workspace_path(arg, must_exist=True)
        content = path.read_text(encoding="utf-8")
    else:
        content = arg
    res = validate_schema_json(content)
    print(json.dumps(res, indent=2))
