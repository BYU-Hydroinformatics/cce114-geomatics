"""MkDocs hooks for the local preview only (see mkdocs.preview.yml).

The lecture pages link to slide decks by absolute published URL, e.g.

    https://byu-hydroinformatics.github.io/cce114-geomatics/slides/day-02/gis-data-models.html

That is correct for the real site, but in a local preview it means clicking a deck
link silently loads the *published* deck — so you would review last week's material
while believing you were looking at your edits. This rewrites those links to the
local server, where tools/preview.sh has built the decks from your working tree.

Nothing here runs during a CI build.
"""

PROD_BASE = "https://byu-hydroinformatics.github.io/cce114-geomatics/"


def on_post_page(output: str, page=None, config=None) -> str:
    """Repoint published-site links at the local server."""
    if PROD_BASE not in output:
        return output
    return output.replace(PROD_BASE, "/")


def on_post_build(config=None, **kwargs) -> None:
    print(
        "\n  Local preview ready.\n"
        "    site   http://localhost:8000/\n"
        "    decks  http://localhost:8000/slides/day-NN/<slug>.html\n"
        "  Deck links on lecture pages now point at your local copies.\n"
    )
