College Inspection System
A simple full-stack web application for managing engineering college inspections.
Built with Flask, SQLite, and Bootstrap.

Project Structure
pgsql
Copy
Edit

Setup Instructions
1. Clone the Repository
bash
Copy
Edit
git clone https://github.com/your-username/college-inspection-system.git
cd college-inspection-system
2. (Optional) Create a Virtual Environment
bash
Copy
Edit
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate # Mac/Linux
3. Install the Dependencies
bash
Copy
Edit
pip install -r requirements.txt
4. Initialize the Database
bash
Copy
Edit
flask --app app.py init-db
5. Run the Application
bash
Copy
Edit
flask --app app.py run
Visit: http://127.0.0.1:5000/ in your browser.

Application Features
Add and manage colleges.

Add and manage departments under each college.

Record inspection events for colleges.

Define evaluation criteria for inspections.

Record detailed inspection ratings based on criteria.

Responsive frontend built using Bootstrap.

Data persistence using SQLite with proper relational design.

