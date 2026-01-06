import json
import requests

class NarrativeExtractor:
    def __init__(self):
        # 1. Ollama Configuration
        # Ensure you have run: 'ollama pull mistral' (or llama3, phi3)
        self.model = "mistral" 
        self.api_url = "http://localhost:11434/api/generate"

        # 2. The EXACT System Prompt (Same as Gemini)
        # Note: We removed "Character: {character}" from the top because 
        # we inject it dynamically in the method below.
        self.system_prompt = """
        You are an expert literary analyst. Analyze the text for character: "{character}".
        Extract structured data strictly following these JSON schemas.

        OUTPUT FORMAT:
        {
          "events": [
            {
              "description": "What happened",
              "event_type": "action|dialogue|thought|memory|dream",
              "time_reference": "childhood|age 15|current|etc",
              "is_flashback": boolean,
              "is_dream": boolean
            }
          ],
          "attributes": [
            {
              "attr_type": "physical|family|occupation|location|trait",
              "attr_name": "Specific name (e.g., eye_color, birthplace)",
              "attr_value": "Extracted value",
              "confidence": "explicit|implied|inferred"
            }
          ],
          "relations": [
            {
              "relation_type": "family|romantic|professional|friend",
              "relation_name": "Specific relation (e.g., father_of, works_for)",
              "target": "Name of the other character"
            }
          ]
        }

        RULES:
        1. "is_dream" and "is_flashback" default to false unless text indicates otherwise.
        2. Only extract info relevant to "{character}".
        3. If no data is found for a category, return an empty list [].
        """

    def extract_from_chunk(self, text, character_name):
        """
        Sends text to local Ollama instance and returns a Python dictionary.
        """
        # 3. Inject the specific character name into the system prompt
        # This replaces "{character}" with "Elena" (or whoever)
        formatted_system = self.system_prompt.replace("{character}", character_name)

        # 4. Prepare the User Input
        user_prompt = f"Text to analyze:\n{text}"

        # 5. Construct the Ollama Payload
        payload = {
            "model": self.model,
            "system": formatted_system,  # The "Brain" goes here
            "prompt": user_prompt,       # The "Data" goes here
            "stream": False,             # Get one full response, not a stream
            "format": "json",            # CRITICAL: Forces clean JSON output
            "options": {
                "temperature": 0.1       # Low temp for consistency
            }
        }

        try:
            # 6. Call the Local API
            response = requests.post(self.api_url, json=payload)
            response.raise_for_status()
            
            # 7. Parse the Result
            result_json = response.json()
            
            # Ollama returns the text in the 'response' key
            extracted_data = json.loads(result_json['response'])
            return extracted_data

        except Exception as e:
            print(f"Error connecting to Ollama: {e}")
            # Return empty structure on failure so code doesn't crash
            return {"events": [], "attributes": [], "relations": []}

# --- TEST BLOCK ---
if __name__ == "__main__":
    extractor = NarrativeExtractor()
    
    # Test Data
    sample_text = "Elena sat by the window. She remembered her father teaching her to ride a bike in Madrid when she was seven."
    character = "Elena"
    
    print(f"Testing Ollama ({extractor.model}) with full schema...")
    result = extractor.extract_from_chunk(sample_text, character)
    
    print(json.dumps(result, indent=2))