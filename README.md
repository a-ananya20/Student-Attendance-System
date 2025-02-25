# Student Attendance System
A web-based Student Attendance System built with Django, HTML, CSS, and JavaScript. It allows admins to manage faculty and students, and faculty to mark attendance and generate reports.

Features

- **Admin Module**:
  - Assign subjects to faculty
  - Manage students and faculty (CRUD operations)
  - 
- **Faculty Module**:
  - Mark student attendance
  - View attendance reports
  
- **General Features**:
  - Secure login system
  - Database integration with MariaDB
  - User-friendly web interface

Tech Stack

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: MariaDB
- **Version Control**: Git, GitHub

Installation & Setup

# Clone the repository
git clone https://github.com/your-username/student-attendance-system.git

# Navigate to project directory
cd student-attendance-system

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure the database (update settings.py for MariaDB)
# Run migrations
python manage.py migrate

# Create a superuser
python manage.py createsuperuser

# Run the development server
python manage.py runserver


