from app import db, SuccessStory

# Delete all entries in the SuccessStory table
def delete_all_stories():
    try:
        # Delete all success story entries
        db.session.query(SuccessStory).delete()
        db.session.commit()  # Commit the changes to the database
        print("All success stories have been deleted successfully.")
    except Exception as e:
        # In case of an error, rollback the session
        db.session.rollback()
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    delete_all_stories()