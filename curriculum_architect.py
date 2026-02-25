import os
import sys
import json
import google.generativeai as genai

# --- 1. CONNECT TO THE BRAIN ---
# This imports the 'search_brain' function from the simula.py you built earlier.
try:
    from simula import load_brain, search_brain
except ImportError:
    print("⚠️  Warning: 'simula.py' not found.")
    print("    Make sure you are in the 'ai-knowledge-graph' folder.")
    # Mock functions so it doesn't crash if file is missing
    def load_brain(files): return []
    def search_brain(kb, query): return []

# --- 2. CONFIGURATION ---
api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    print("❌ Error: GOOGLE_API_KEY is not set.")
    sys.exit(1)

genai.configure(api_key=api_key)
# Using the reasoning model (System 2)
model = genai.GenerativeModel('gemini-flash-latest') 

# --- 3. THE ARCHITECT ---
def design_training_pack(task_description, robot_type):
    print(f"🧠 ACTIVATING BRAIN: Searching internal knowledge for '{task_description}'...")
    
    # A. LOAD KNOWLEDGE (Pre-Computation)
    # We load the graphs we built from your PDFs
    brain_files = ["pinns_brain.json", "the_well_brain.json"]
    knowledge_base = load_brain(brain_files)
    
    # B. QUERY THE BRAIN
    # We look for physics constraints (turbulence, shock waves, etc.)
    if knowledge_base:
        print("   ↳ Scanning Knowledge Graph for physics constraints...")
        # Search for failure modes relevant to simulation
        search_results = search_brain(knowledge_base, "physics failure simulation")
        
        # If the specific search fails, try a broader one
        if not search_results:
             search_results = search_brain(knowledge_base, "dataset simulation")
             
        context = "\n".join(search_results[:15])
        print(f"   ↳ Found {len(search_results)} relevant insights.")
    else:
        context = "No internal knowledge available."

    # C. DESIGN THE BLUEPRINT
    print(f"🏭 DATA FACTORY: Architecting the Training Pack...")

    prompt = f"""
    You are the Chief Data Architect for a Robotics Data Factory.
    We are using the 'Simula' framework (Taxonomies for Global Coverage).
    
    INTERNAL RESEARCH (Context):
    {context}
    
    TASK: {task_description}
    ROBOT: {robot_type}
    
    GOAL: Design a "Training Pack" (Dataset Blueprint) for Isaac Sim.
    
    INSTRUCTIONS:
    1. If the Internal Research mentions specific equations (e.g. Navier-Stokes, Burgers), use them.
    2. Define "Edge Cases" based on physics failures (turbulence, friction loss).
    3. Output valid JSON only.
    
    OUTPUT JSON STRUCTURE:
    {{
      "training_pack_id": "pack_001_grounded",
      "scientific_basis": "Derived from Internal Knowledge Graph",
      "curriculum_stages": [
        {{
            "stage_name": "nominal_baseline",
            "description": "Standard operating conditions",
            "iterations": 10,
            "parameters": {{ "lighting": "uniform", "physics_fidelity": "low" }}
        }},
        {{
            "stage_name": "scientific_stress_test",
            "description": "Testing specific physics failures",
            "iterations": 100,
            "parameters": {{ 
                "equation_type": "string", 
                "surface_friction": [0.1, 0.9],
                "notes": "Testing specific failure mode"
            }}
        }}
      ]
    }}
    """
    
    try:
        response = model.generate_content(prompt)
        clean_json = response.text.replace("```json", "").replace("```", "").strip()
        data = json.loads(clean_json)
        return data
    except Exception as e:
        print(f"❌ Thinking Error: {e}")
        return None

# --- 4. EXECUTION ---
if __name__ == "__main__":
    task = "Manipulate liquid container with shock wave potential"
    robot = "Frank Emika Panda"
    
    blueprint = design_training_pack(task, robot)
    
    if blueprint:
        filename = "grounded_training_pack.json"
        with open(filename, "w") as f:
            json.dump(blueprint, f, indent=2)
            
        print(f"\n✅ CURRICULUM ARCHITECTED. Saved to {filename}")
        print("   This blueprint forces the simulator to solve the 'Edge Cases'.")
        print("-" * 50)
        print(json.dumps(blueprint, indent=2))
        print("-" * 50)

