import os
import sys
import json
import google.generativeai as genai

# --- 1. CONFIGURATION ---
api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    print("❌ Error: GOOGLE_API_KEY is not set.")
    sys.exit(1)

genai.configure(api_key=api_key)
# Using the stable model to avoid rate limits
model = genai.GenerativeModel('gemini-flash-latest')

# --- 2. BRAIN LOADER ---
def load_brain(filenames):
    """Loads knowledge from multiple JSON files."""
    knowledge = []
    print("🧠 Simula is waking up...")
    
    for filename in filenames:
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                
                # Case 1: List of facts
                if isinstance(data, list):
                    knowledge.extend(data)
                
                # Case 2: Graph dictionary
                elif isinstance(data, dict) and "links" in data:
                    for link in data["links"]:
                        knowledge.append({
                            "subject": link["source"],
                            "predicate": link.get("id", "related_to"),
                            "object": link["target"]
                        })
            print(f"  ✅ Connected to memory bank: {filename}")
        except FileNotFoundError:
            print(f"  ⚠️ Warning: Memory bank missing: {filename}")
            
    return knowledge

# --- 3. SMART SEARCH ENGINE ---
def search_brain(knowledge, query):
    """Finds relevant facts by checking for keywords."""
    results = []
    
    # Break the user's sentence into keywords (ignore small words)
    ignore_words = {"what", "is", "how", "do", "i", "the", "a", "an", "in", "of", "to", "for", "are"}
    keywords = [w for w in query.lower().split() if w not in ignore_words]
    
    print(f"  🔍 Scanning for keywords: {keywords}")
    
    for item in knowledge:
        s = str(item.get("subject", "")).lower()
        o = str(item.get("object", "")).lower()
        
        # If ANY keyword matches the subject or object
        if any(k in s for k in keywords) or any(k in o for k in keywords):
            fact = f"{item['subject']} is {item['predicate']} {item['object']}"
            results.append(fact)
    
    return results

# --- 4. MAIN INTELLIGENCE ---
if __name__ == "__main__":
    # Load the Brains
    brain_files = ["pinns_brain.json", "the_well_brain.json"]
    knowledge_base = load_brain(brain_files)
    
    # Check for User Question
    if len(sys.argv) < 2:
        print("\n🔮 SIMULA ONLINE.")
        print("Usage: python3 simula.py \"How do I simulate fluids?\"")
        sys.exit(0)
        
    user_query = sys.argv[1]
    print(f"\n🤔 Thinking about: '{user_query}'...")
    
    # Retrieve Facts
    facts = search_brain(knowledge_base, user_query)
    
    if not facts:
        print("❌ I searched my memory, but found no specific data on that.")
        sys.exit(0)
        
    print(f"🔍 Retrieved {len(facts)} data points.")
    
    # Generate Answer
    context = "\n".join(facts[:50]) # Use top 50 facts
    prompt = f"""
    You are Simula, an expert AI Physics Architect.
    You have retrieved the following specific facts from your internal database:
    
    --- DATA START ---
    {context}
    --- DATA END ---
    
    USER QUESTION: {user_query}
    
    INSTRUCTIONS:
    1. Answer the user's question using ONLY the data provided above.
    2. Be technical but clear.
    3. Cite the specific datasets or methods mentioned in the data.
    
    ANSWER:
    """
    
    response = model.generate_content(prompt)
    print("\n" + "="*50)
    print(response.text)
    print("="*50 + "\n")
