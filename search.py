import json
import sys

# 1. Check for search term
if len(sys.argv) < 2:
    print("Usage: python3 search.py <search_term>")
    sys.exit(1)

query = sys.argv[1].lower()
filename = "the_well_brain.json"

print(f"🔍 Searching for '{query}' in {filename}...\n")

try:
    with open(filename, "r") as f:
        data = json.load(f)

    found = False

    # Check if data is a List (Simple JSON)
    if isinstance(data, list):
        for item in data:
            s = str(item.get("subject", "")).lower()
            o = str(item.get("object", "")).lower()
            if query in s or query in o:
                found = True
                print(f"  ⭐ {item['subject']} --[{item['predicate']}]--> {item['object']}")

    # Check if data is a Graph (Network JSON)
    elif isinstance(data, dict) and "links" in data:
        for link in data["links"]:
            s = str(link["source"]).lower()
            t = str(link["target"]).lower()
            if query in s or query in t:
                found = True
                print(f"  ⭐ {link['source']} --[{link.get('id', 'related')}]--> {link['target']}")

    if not found:
        print("❌ No connections found.")

except Exception as e:
    print(f"Error: {e}")
