#!/usr/bin/env python3
"""
Scan all Commons main-namespace pages (non-redirects only).
If a page does NOT contain {{gallery page}},
print the page title and the Commons category from Wikidata (P373), if any.
"""

import re
import pywikibot
from pywikibot import Page, ItemPage

GALLERY_TEMPLATE_RE = re.compile(r'\{\{\s*gallery\s*page\b', re.IGNORECASE)


def has_gallery_template(page: Page) -> bool:
    """Return True if {{gallery page}} is found in the page text."""
    try:
        text = page.get()
    except Exception:
        return False
    return bool(GALLERY_TEMPLATE_RE.search(text))


def get_p373(page: Page):
    """Return Commons category (P373) from Wikidata item, or None."""
    try:
        item = ItemPage.fromPage(page)
        item.get()
    except Exception:
        return None

    claims = item.claims.get("P373")
    if not claims:
        return None

    try:
        return claims[0].getTarget()
    except Exception:
        return None


def main():
    site = pywikibot.Site("commons", "commons")

    # Iterate over all NON-REDIRECT pages in main namespace
    for page in site.allpages(namespace=0, filterredir=False):
        # Extra safety check (cheap, no API call)
        if page.isRedirectPage():
            continue

        if has_gallery_template(page):
            continue

        commons_cat = get_p373(page)

        if commons_cat:
            print(f"{page.title()} → Category:{commons_cat}")
            page.text = page.get()
            page.text = "{{gallery page|1=" + commons_cat + "}}\n" + page.text
            try:
                page.save('[[User:MatrixBot|Task 8]]: Add {{gallery page}} to galleries')
                print(f"Page '{page.title()}' saved successfully.")
            except pywikibot.exceptions.EditConflictError:
                print(f"Edit conflict occurred on '{page.title()}'.")
            except pywikibot.exceptions.NoPageError:
                print(f"Page '{page.title()}' does not exist.")
            except pywikibot.exceptions.IsRedirectPageError:
                print(f"Page '{page.title()}' is a redirect page. Cannot save directly.")
            except pywikibot.exceptions.LockedPageError:
                print(f"Page '{page.title()}' is locked. Cannot save.")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
        else:
            print(f"{page.title()} → (no P373 on Wikidata)")


if __name__ == "__main__":
    main()
