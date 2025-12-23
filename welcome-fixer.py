#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# icl half of this is ChatGPT

import re
import urllib.parse
import pywikibot
from pywikibot import pagegenerators

# -------------------------------
# USER CONFIGURATION
# -------------------------------
SEARCH_URL = "https://commons.wikimedia.org/w/index.php?search=insource%3A%2FSimply+upload+the+file+again+and+mark+the+old+one+like+this%3A+%5C%3Ctt%5C%3E%2F&title=Special%3ASearch&profile=advanced&fulltext=1&ns0=1&ns1=1&ns2=1&ns3=1&ns4=1&ns5=1&ns6=1&ns7=1&ns8=1&ns9=1&ns10=1&ns11=1&ns12=1&ns13=1&ns14=1&ns15=1&ns100=1&ns101=1&ns102=1&ns103=1&ns104=1&ns105=1&ns106=1&ns107=1&ns460=1&ns461=1&ns486=1&ns487=1&ns828=1&ns829=1&ns1198=1&ns1199=1&ns2300=1&ns2301=1&ns2302=1&ns2303=1"

REGEX_PATTERN = r"""(?s)(<div style="font-size:110%;">'''Welcome to Wikimedia Commons, .*?'''</div>.*?this message\?\)</small>\n\|\})"""
REGEX_REPLACEMENT = "{{Welcome}}"

EDIT_SUMMARY = "[[User:MatrixBot|Task 7]]: Unsubstitute {{welcome}} template"
DRY_RUN = False  # Set to True to preview changes without saving

# -------------------------------
# PARSE SEARCH URL
# -------------------------------
parsed = urllib.parse.urlparse(SEARCH_URL)
query = urllib.parse.parse_qs(parsed.query)

search_string = query.get("search", [""])[0]

# -------------------------------
# INITIALIZE WIKI SITE
# -------------------------------
site = pywikibot.Site("commons", "commons")
site.login()

# -------------------------------
# GENERATE PAGES FROM SEARCH
# -------------------------------
generator = pagegenerators.SearchPageGenerator(
    search_string,
    site=site,
    total=None
)

preload_gen = pagegenerators.PreloadingGenerator(generator)

# -------------------------------
# PROCESS PAGES
# -------------------------------
for page in preload_gen:
    if not page.exists():
        continue

    try:
        text = page.get()
    except Exception as e:
        print(f"Could not retrieve {page.title()}: {e}")
        continue

    new_text = re.sub(REGEX_PATTERN, REGEX_REPLACEMENT, text)

    if new_text == text:
        print(f"No change in {page.title()}")
        continue

    print(f"Changes found in {page.title()}")

    if not DRY_RUN:
        try:
            page.put(new_text, summary=EDIT_SUMMARY)
            print(f"Saved: {page.title()}")
        except Exception as e:
            print(f"Error saving {page.title()}: {e}")
    else:
        print("--- DRY RUN: Changes not saved ---")
