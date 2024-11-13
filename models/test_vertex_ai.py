import vertexai
from vertexai.generative_models import GenerativeModel
import json
import re

# Initialize Vertex AI
vertexai.init(project="mini-proj-mca", location="us-central1")

# Select the model
model = GenerativeModel("gemini-1.5-flash-002")

# Request for pure JSON output with clear instruction
response = model.generate_content(
    "IMPORTANT: JUST GENERATE PURE JSON CODE. DO NOT ADD ANY EXTRANEOUS TEXT, LABELS, OR EXPLANATIONS. "
    "THE OUTPUT SHOULD ONLY BE A VALID JSON OBJECT THAT CAN BE PASSED TO A PARSE FUNCTION. "
    "The JSON should be structured as follows:\n"
    "{\n"
    "  \"quiz\": [\n"
    "    {\"question\": \"<question1>\", \"options\": [\"A\", \"B\", \"C\", \"D\"]},\n"
    "    {\"question\": \"<question2>\", \"options\": [\"A\", \"B\", \"C\", \"D\"]},\n"
    "    ...\n"
    "  ]\n"
    "}\n"
    "Profile Information:\n"
    "Academic: MCA\n"
    "Interests: AI\n"
    "Target Industry: Computer\n"
    "Skills: Nothing\n"
)

# Clean up the response to extract the JSON content
try:
    # Look for JSON structure in the response using regex
    json_match = re.search(r'(\{.*\})', response.text.strip(), re.DOTALL)
    
    if json_match:
        json_data = json_match.group(1)  # Extract the JSON string
        parsed_json = json.loads(json_data)  # Parse into Python dictionary
        print(json.dumps(parsed_json, indent=2))  # Pretty print JSON
    else:
        print("No valid JSON found in the response.")

except Exception as e:
    print(f"Error processing the response: {e}")
