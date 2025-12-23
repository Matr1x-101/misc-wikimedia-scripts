# The code was copied from Qwerfjkl's code on Wikipedia and changes were made
# CC-BY-SA-4.0 https://creativecommons.org/licenses/by-sa/4.0/deed.en
# Changes by Matrix can be licensed under GPLv3, per one-way compatibility

import regex as re
from urllib.parse import urlparse, parse_qs
import pywikibot
from pywikibot import pagegenerators
site=pywikibot.Site("commons:commons")
def parse_text_file(file_path):
    parsed_data = []
    # Read the file content
    with open(file_path, 'r') as file:
        content = file.read()
    # Split the content based on occurrences of URLs starting with 'https://en.wikipedia.org'
    sections = re.split(r'(https://commons\.wikimedia\.org[^\`]*)', content)
    # Iterate over the sections
    for i in range(1, len(sections), 2):  # Start at 1 and step by 2 to access the URL sections
        search_url = sections[i].strip()  # The search URL part (fine to trim because search URL is just wrapper for search query)
        # Get the remaining part (i+1) and split by the `` delimiter
        if i + 1 < len(sections):
            parts = sections[i + 1].split('``')

            # Ensure there are exactly 3 parts: search URL, find strings, and replacement strings
            if len(parts) == 3:
                find_strings = parts[1].split('`') # shouldn't need strip
                replacement_strings = parts[2].rstrip("\n").split('`') # catch trailing newlines just in case; maybe bug
                # Append the parsed data
                parsed_data.append({
                    'search_url': parse_qs(urlparse(search_url).query)['search'][0],
                    'find_strings': find_strings,
                    'replacement_strings': replacement_strings
                })
    return parsed_data
file_path = 'Wikilint7a-v2.txt'
parsed_data = parse_text_file(file_path)
for entry in parsed_data:
    print(entry["search_url"])
    print(entry["find_strings"][0])
    print(entry['replacement_strings'][0], end="\n\n")

titles=[]
replacements=[]
# Display parsed data
for entry in parsed_data:
    gen = pagegenerators.SearchPageGenerator(entry['search_url'], site=site)
    print(f"Searching for {entry['search_url']}")
    title_count = 0
    for title in gen:
        titles.append(title)
        title_count+=1
    print("Total titles found:", title_count)
    if len(entry['find_strings']) >= 2 or len(entry['replacement_strings']) >= 2:
        if len(entry['find_strings']) == len(entry['replacement_strings']):
            for i in range(len(entry['find_strings'])):
                replacements.append([entry['find_strings'][i], entry['replacement_strings'][i]])
        else:
            raise Exception
    else:
        replacements.append([entry['find_strings'][0], entry['replacement_strings'][0]])
#     print(f"Search URL: {entry['search_url']}")
#     print(f"Find Strings: {entry['find_strings']}")
#     print(f"Replacement Strings: {entry['replacement_strings']}")
#     print("-" * 40)

# from pprint import pprint
# pprint(replacements)
# print(len(replacements))
titles = list(set(titles))
print(len(titles))
# print(titles)
import random
edits_left = float("infinity")
trial_titles = titles
# trial_titles.insert(0, pywikibot.Page(site, "Talk:Meal, Ready-to-Eat/Archive 1")) # debug
for page in trial_titles:
    print("Handling", page.title())
    oldtext = page.text
    text = oldtext
    for replacement in replacements:
        # Use regex instead of plain string replace
        text = re.sub(replacement[0], replacement[1], text)
    if oldtext == text:
        continue
    if edits_left <= 0:
        break
    page.text = text
    try:
        page.save("Fixing [[mw:Special:MyLanguage/Help:Lint errors|lint errors]] ([[User:MatrixBot|task 6]])", bot=True, minor=True)
        edits_left -= 1
    except Exception as e:
        print("Error:", e)

    # print(len(titles))
# print(titles)
