# The-Secret-Garden
A flower shop app - My final project for the Python Web course of SoftUni

## **Setup Instructions**

Follow these steps to set up and run the project on your local machine.

### **1. Download the Code**
Clone the repository to your local machine:
```
git clone <repository_url>
cd <project_folder>
```

### **2. Set Up the Python Environment**
  python -m venv venv
  source venv/bin/activate  # On Linux/macOS
  venv\Scripts\activate     # On Windows

Install the required Python dependencies:
  pip install -r requirements.txt

### **3. Install Node.js**
  npm install

### **4. Configure Environment Variables**
Create a .env file
Paste the privately provided credentials
Update the DB_HOST value based on your setup:
-On Linux: Use the IP address of your host machine. Run ip addr show to find it.
-On macOS/Windows: Use host.docker.internal. (if using  Docker)

### **5. Set Up the Database**
Run migrations to create the database schema:
  python manage.py migrate

Populate the database with initial data:
Copy the contents of the privately provided Pastebin link into a file named data.json (save it in the same directory as manage.py).
Load the data:
  python manage.py loaddata data.json
This will populate the database with:
- Sample products (flowers and gifts).
- Predefined groups and their permissions.

### **6. Create Users**
Create a superuser to access the admin panel:
  python manage.py createsuperuser
Staff Users: Add staff users through the admin panel. When selecting their role, they will automatically be assigned to the correct group with the appropriate permissions.
Customers: Customers can register directly through the application’s registration page. They will automatically be assigned to the "Customer" group.

### **7. Run the Server**
  python manage.py runserver

Notes:
Admin Panel Permissions: Group permissions for the admin panel are assigned automatically based on roles.
Frontend Permissions: These are managed separately using custom permission mixins.
