from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from models.ai_model import generate_quiz, generate_roadmap_func
import os

# Initialize the Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24) 

# Configure SQLite database for storing user credentials
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///career_mapping.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Define SuccessStory model for storing success stories
class SuccessStory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    academic_grades = db.Column(db.String(120), nullable=False)
    skills = db.Column(db.String(250), nullable=False)
    roadmap = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default="pending", nullable=False)


# Define User model for storing login information
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Create the database and add a default user if it doesn't already exist
with app.app_context():
    db.create_all()
    if not User.query.filter_by(username='gazam').first():
        user = User(username='gazam', password='password123')
        db.session.add(user)
        db.session.commit()
        
    if not User.query.filter_by(username='admin').first():
       admin = User(username='admin', password='adminpass')
       db.session.add(admin)
       db.session.commit()

# Home route, displays the welcome page
@app.route("/")
def home():
    return render_template("home.html")

# Login route, displays the login form
@app.route("/loginpage")
def loginpage():
    return render_template("login.html", title="Login")

# Authentication route, validates user credentials
@app.route("/afterlogin", methods=["POST"])
def afterlogin():
    username = request.form.get("uname")
    password = request.form.get("pass")
    user = User.query.filter_by(username=username, password=password).first()
    if user:
        session['username'] = username
        flash(f"Welcome, {username}!", "success")
        return redirect(url_for("dashboard"))
    flash("Invalid credentials. Please try again.", "danger")
    return redirect(url_for("loginpage"))

# Dashboard route, displays main options
@app.route("/dashboard")
def dashboard():
    if 'username' not in session:
        return redirect(url_for("loginpage"))
    return render_template("dashboard.html", username=session['username'], title="Dashboard")

# Career Recommendations route, displays a form for recommendations
@app.route("/career_recommendations")
def career_recommendations():
    if 'username' not in session:
        return redirect(url_for("loginpage"))
    return render_template("career_recommendations.html")


@app.route("/generate_quiz_page", methods=["POST"])
def generate_quiz_page():
    if 'username' not in session:
        return redirect(url_for("loginpage"))
    
    # Collect user data from the form
    user_data = {
        "academic": request.form.get("academic"),
        "interests": request.form.get("interests"),
        "target_industry": request.form.get("target_industry"),
        "skills": request.form.get("skills")
    }

    # Store user data in session for later use
    session['user_data'] = user_data

    # Generate quiz using the AI model
    quiz_data = generate_quiz(user_data)

    # Check if the quiz_data is a dictionary
    if not isinstance(quiz_data, dict):
        flash("Invalid quiz data format received.", "danger")
        return redirect(url_for("home"))

    # Pass the quiz data to the template
    return render_template("quiz.html", quiz_data=quiz_data)


# Generate Roadmap route, sends quiz answers to Vertex AI and displays roadmap
@app.route("/generate_roadmap", methods=["POST"])
def generate_roadmap():
    if 'username' not in session:
        return redirect(url_for("loginpage"))
    
    quiz_answers = request.form.getlist("answers[]")
    # Retrieve user data from session
    user_data = session.get('user_data', {})
    # Generate roadmap using AI model
    roadmap = generate_roadmap_func(user_data, quiz_answers)
    return render_template("roadmap.html", roadmap=roadmap.get("roadmap", []))


# Success Stories
@app.route("/success_stories", methods=["GET", "POST"])
def success_stories():
    if request.method == "POST":
        try:
            # Save the submitted success story to the database
            new_story = SuccessStory(
                username=session.get("username", "Anonymous"),  # Get username from session
                academic_grades=request.form.get("academic_grades"),
                skills=request.form.get("skills"),
                roadmap=request.form.get("roadmap")
            )
            db.session.add(new_story)
            db.session.commit()  # Commit the transaction to save in the database
            
            flash("Your success story has been submitted!", "success")
            return redirect(url_for("success_stories"))  # Redirect to the success stories page after submission

        except Exception as e:
            # Handle any database or form submission errors
            db.session.rollback()  # Rollback in case of error
            flash(f"An error occurred: {str(e)}", "danger")
            return redirect(url_for("success_stories"))

    return render_template("success_stories.html")  


@app.route("/view_success_stories")
def view_success_stories():
    if 'username' not in session:
        return redirect(url_for("loginpage"))

    # Retrieve all success stories from the database
    stories = SuccessStory.query.all()

    # Render the page that displays all success stories
    return render_template("view_success_stories.html", stories=stories)

# Admin panel route for managing success stories
@app.route("/admin_loginpage")
def admin_loginpage():
    return render_template("admin_login.html", title="Admin Login")     

@app.route("/admin_afterlogin", methods=["POST"])
def admin_afterlogin():
    username = request.form.get("uname")
    password = request.form.get("pass")
    
    # Check if admin credentials are correct
    admin_user = User.query.filter_by(username=username, password=password).first()
    
    if admin_user and admin_user.username == "admin":
        session['admin'] = True  # Mark this session as admin
        flash(f"Welcome Admin, {username}!", "success")
        return redirect(url_for("admin_panel"))  # Redirect to the admin panel
    
    flash("Invalid admin credentials. Please try again.", "danger")
    return redirect(url_for("admin_loginpage"))


@app.route("/admin")
def admin_panel():
    # Check if admin is logged in
    if not session.get('admin'):
        flash("You need to be an admin to access this page.", "danger")
        return redirect(url_for("admin_loginpage"))  # Redirect to admin login page if not an admin

    # Fetch all success stories
    stories = SuccessStory.query.all()

    return render_template("admin_panel.html", stories=stories)


@app.route("/approve_story/<int:story_id>")
def approve_story(story_id):
    # Check if the user is admin
    if not session.get('admin'):
        flash("You need to be an admin to perform this action.", "danger")
        return redirect(url_for("admin_loginpage"))
    
    story = SuccessStory.query.get_or_404(story_id)
    story.status = "approved"  # Mark as approved
    db.session.commit()
    flash("Story approved successfully!", "success")
    return redirect(url_for("admin_panel"))  # Redirect to the admin panel

@app.route("/delete_story/<int:story_id>")
def delete_story(story_id):
    # Check if the user is admin
    if not session.get('admin'):
        flash("You need to be an admin to perform this action.", "danger")
        return redirect(url_for("admin_loginpage"))
    
    story = SuccessStory.query.get_or_404(story_id)
    db.session.delete(story)
    db.session.commit()
    flash("Story deleted successfully!", "success")
    return redirect(url_for("admin_panel"))  # Redirect to the admin panel




# Logout route, clears session data and redirects to login
@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("loginpage"))

# Logout route, clears session data and redirects to login
@app.route("/admin_logout")
def admin_logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("admin_loginpage"))


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
