from langchain.prompts import PromptTemplate

# SIMULA PHYSICS LOGIC
system_prompt = """
You are an expert Industrial Physics Engineer building a reliability database.
Your goal is to extract CAUSAL CHAINS of physical failure from the provided text.

Format output as triplets: (Subject, Predicate, Object).

RULES:
1. Ignore generic info (dates, intros).
2. Focus on Material Properties (Friction, Specular, Mass).
3. Focus on Sensor Failures (Lidar Noise, IR Saturation, Occlusion).
4. Focus on Environmental Risks (Dust, Glare, Vibration).

EXAMPLES:
- Text: "Oily metal surfaces reduce friction causing gripper slip."
  -> (Oily Metal, reduces, Friction)
  -> (Low Friction, causes, Slip Failure)
"""

def get_extraction_prompt():
    return PromptTemplate(
        template=system_prompt + "\n\nTEXT TO ANALYZE:\n{text}\n\nTRIPLETS:",
        input_variables=["text"]
    )
