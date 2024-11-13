import vertexai
from vertexai.generative_models import GenerativeModel
import json
import re

# Initialize Vertex AI
vertexai.init(project="mini-proj-mca", location="us-central1")

# Initialize the generative model
model = GenerativeModel("gemini-1.5-flash-002")

def generate_quiz(user_data):
    prompt = (
        "You have to ask at least 5 question and maximum of 8 questions"
        "based on the exisiting skills you have to modify the level of questions."
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
        f"Academic: {user_data['academic']}\n"
        f"Interests: {user_data['interests']}\n"
        f"Target Industry: {user_data['target_industry']}\n"
        f"Skills: {user_data['skills']}\n"
        )

    # Generate quiz content using AI model
    response = model.generate_content(prompt)  # Assuming you're using Vertex AI or similar
    
    try:
        json_match = re.search(r'(\{.*\})', response.text.strip(), re.DOTALL)
    
        if json_match:
            json_data = json_match.group(1) 
            parsed_json = json.loads(json_data) 
            return parsed_json
        else:
            print("No valid JSON found in the response.")

    except Exception as e:
        print(f"Error processing the response: {e}")

def generate_roadmap_func(user_data, quiz_answers):
    prompt = (
        "Generate a personalized career roadmap in JSON format based on the following profile "
        "and quiz answers. This roadmap should include actionable steps for the user's career "
        "path in the target industry. Please provide clear guidance on necessary skills, certifications, education, "
        "and experiences to achieve career goals.\n\n"
        f"Academic Performance: {user_data.get('academic')}\n"
        f"Interests: {user_data.get('interests')}\n"
        f"Target Industry: {user_data.get('target_industry')}\n"
        f"Skills: {user_data.get('skills')}\n\n"
        f"Quiz Answers: {quiz_answers}\n\n"
        "IMPORTANT: JUST GENERATE PURE JSON CODE. DO NOT ADD ANY EXTRANEOUS TEXT, LABELS, OR EXPLANATIONS. "
        "THE OUTPUT SHOULD ONLY BE A VALID JSON OBJECT THAT CAN BE PASSED TO A PARSER FUNCTION. "
        "Structure the JSON output as follows:\n"
        "{\n"
        "  \"roadmap\": [\n"
        "    {\"title\": \"<Step 1>\", \"description\": \"<Details for Step 1>\"},\n"
        "    {\"title\": \"<Step 2>\", \"description\": \"<Details for Step 2>\"},\n"
        "    ...\n"
        "  ]\n"
        "}"
    )

    # Generate roadmap content using the AI model
    response = model.generate_content(prompt)

    try:
        # Extract JSON from the response using regex
        json_match = re.search(r'(\{.*\})', response.text.strip(), re.DOTALL)

        if json_match:
            json_data = json_match.group(1)
            parsed_json = json.loads(json_data)  # Convert the extracted JSON string to a Python dictionary
            return parsed_json
        else:
            print("No valid JSON found in the response.")
            return {"error": "No valid JSON found in the response."}

    except Exception as e:
        print(f"Error processing the response: {e}")
        return {"error": f"Error processing the response: {e}"}