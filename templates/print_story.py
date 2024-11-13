from app import app
from app import SuccessStory

# Run the script in the Flask app context
with app.app_context():
    # Fetch all success stories from the database
    stories = SuccessStory.query.all()

    # Print each story
    for story in stories:
        print(f"ID: {story.id}")
        print(f"Username: {story.username}")
        print(f"Academic Grades: {story.academic_grades}")
        print(f"Skills: {story.skills}")
        print(f"Roadmap: {story.roadmap}")
        print("-" * 40)  # Just a separator for readability
