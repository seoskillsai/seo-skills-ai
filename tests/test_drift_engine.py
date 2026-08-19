import pytest
from scripts.parse_html import parse_html_content

def test_parse_html_content():
    sample_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Title</title>
        <meta name="description" content="Test description" />
        <link rel="canonical" href="https://example.com/test" />
    </head>
    <body>
        <h1>Primary Heading</h1>
        <h2>Secondary Heading</h2>
        <p>This is a paragraph with some content for testing word counts.</p>
    </body>
    </html>
    """
    res = parse_html_content(sample_html)
    assert res["title"] == "Test Title"
    assert res["meta_description"] == "Test description"
    assert res["canonical"] == "https://example.com/test"
    assert res["h1"] == ["Primary Heading"]
    assert res["h2"] == ["Secondary Heading"]
    assert res["word_count"] > 5
