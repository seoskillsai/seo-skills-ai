#!/usr/bin/env python3
"""Google API credential status. Live calls live in gsc_query.py and ga4_report.py."""
import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.google_oauth import get_tier_status, setup_interactive

if __name__ == "__main__":
    if "--setup" in sys.argv:
        raise SystemExit(setup_interactive())
    status = get_tier_status()
    print(json.dumps(status, indent=2))
