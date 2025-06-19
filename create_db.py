from app import db, app
from app import Signup, Contact_table, Posts  

# Create the database tables in the connected database 
with app.app_context():
    db.create_all()
    print("All tables created successfully in your local database.")
