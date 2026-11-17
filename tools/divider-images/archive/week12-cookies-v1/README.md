# Cookie-cutter series, version 1 (backup)

The six images used on the Day 22 "Site selection is cookie cutting" slide and in the Day 23
Workflow Walkthrough deck from 2026-11-17 (commit 757d09d), before the geographically accurate
version (tools/generate_cookie_series.py) replaced them the same day. `prompts.json` was
tools/divider-images/week12-cookies.json until then. They are generic shapes, not the real Utah County, I-15 buffer or store
locations. `prompts.json` holds the prompts (gpt-image-2.5-flare; panel 4 regenerated with
gpt-image-2.5-sunburst using the prompt shown).

To roll back, copy these files over the same names in both deck folders:

    cp tools/divider-images/archive/week12-cookies-v1/ws-cookie-*.jpg slides/day-22/images/
    cp tools/divider-images/archive/week12-cookies-v1/ws-cookie-*.jpg slides/day-23/images/
