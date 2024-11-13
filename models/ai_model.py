import vertexai
from vertexai.generative_models import GenerativeModel

# Initialize Vertex AI with the project ID and location
vertexai.init(project="mini-proj-mca", location="us-central1")

# Initialize the generative model
model = GenerativeModel("gemini-1.5-flash-002")

def generate_roadmap(user_data, quiz_answers):
    """
    Generates a roadmap in JSON format based on user data and quiz answers.

    Args:
    user_data (dict): A dictionary containing user's initial input data such as academic grades,
                      interests, target industry, and skills.
    quiz_answers (list): A list of user's answers to the quiz questions.

    Returns:
    dict: JSON with roadmap recommendations.
    """
    # Create the prompt based on user data and quiz answers
    prompt = (
        "Based on the following user profile and quiz answers, generate a career roadmap in JSON format "
        "with actionable steps for achieving career goals:\n\n"
        f"Academic Performance: {', '.join([f'{s['name']} - {s['marks']}' for s in user_data['subjects']])}\n"
        f"Interests: {user_data['interests']}\n"
        f"Target Industry: {user_data['target_industry']}\n"
        f"Skills: {user_data['skills']}\n\n"
        f"Quiz Answers: {quiz_answers}\n\n"
        "Please structure the JSON response with a list of steps, where each step has a 'title' and 'description':\n"
        "{\n"
        "  \"roadmap\": [\n"
        "    {\"title\": \"<Step 1>\", \"description\": \"<Details for Step 1>\"},\n"
        "    {\"title\": \"<Step 2>\", \"description\": \"<Details for Step 2>\"},\n"
        "    ...\n"
        "  ]\n"
        "}"
    )

    # Generate roadmap content using the generative model
    response = model.generate_content(prompt)

    # Parse the response to extract the JSON roadmap
    roadmap_json = response.text  # Assuming response.text is the JSON structure returned by the model
    return roadmap_json

# Example usage
if __name__ == "__main__":
    # Sample user data and quiz answers
    user_data = {
        "subjects": [
            {"name": "Mathematics", "marks": "85%"},
            {"name": "Science", "marks": "78%"},
            {"name": "English", "marks": "92%"},
            {"name": "Social Studies", "marks": "80%"},
            {"name": "Computer Science", "marks": "88%"}
        ],
        "interests": "Artificial Intelligence, Data Science",
        "target_industry": "Technology",
        "skills": "Python, Machine Learning, Data Analysis"
    }

    quiz_answers = ["A", "B", "C", "D", "A"]  # Sample answers

    # Generate the roadmap based on the user data and quiz answers
    roadmap = generate_roadmap(user_data, quiz_answers)
    print("Generated Roadmap JSON:")
    print(roadmap)
