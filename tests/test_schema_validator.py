import pytest
import json
from scripts.schema_validator import validate_schema_json

def test_valid_article_schema():
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "TechArticle",
                "headline": "Testing SEO"
            }
        ]
    }
    res = validate_schema_json(json.dumps(schema))
    assert res["valid_json"] is True
    assert "TechArticle" in res["types_found"]
    assert len(res["deprecated_warnings"]) == 0

def test_deprecated_howto_schema():
    schema = {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": "How to do SEO"
    }
    res = validate_schema_json(json.dumps(schema))
    assert res["valid_json"] is True
    assert len(res["deprecated_warnings"]) >= 1
    assert "HowTo" in res["deprecated_warnings"][0]
