# The-Secret-Garden
A flower shop web app - My final project for the Python Web course of SoftUni

![image](https://github.com/user-attachments/assets/04b5b2e4-6103-4581-b8dc-d73644ec1a38)

## 🚀 Deployed App
[Visit the deployed app](https://thesecretgarden-bnf4g7hkcrdwajea.italynorth-01.azurewebsites.net/)
- For project evaluators: Please contact me at nalanbilgin@gmail.com for the superuser credentials that you can use on the deployed site! I will write you back in no time :) Otherwise you can install the project locally following the instructions below.

## 🛠️ **Setup Instructions**

Follow these steps to set up and run the project on your local machine.

### **1. Download the Code**
Clone the repository from the main branch to your local machine:
```
git clone <repository_url>
cd <project_folder>
```

### **2. Set Up the Python Environment**
```
python -m venv venv
source venv/bin/activate  # On Linux/macOS
venv\Scripts\activate     # On Windows
```

Install the required Python dependencies:
```
pip install -r requirements.txt
```

### **3. Install Node.js and Dependencies**
Make sure to have Node.js installed and then install the dependencies
```
npm install
```

### **4. Configure Environment Variables**
- Create a .env file.
- Paste the privately provided credentials
- Update the DB_HOST value based on your setup

### **5. Set Up the Database**
- Run migrations to create the database schema:
```
python manage.py migrate
```
- Populate the database with initial data:
- Copy the contents of the privately provided Pastebin link into a file named data.json (save it in the same directory as manage.py).
- Load the data:
```
python manage.py loaddata data.json
```
- This will populate the database with:
  -Sample products (flowers and gifts).
  -Predefined groups and their permissions.

### **6. Create Users**
Create a superuser to access the admin panel:
```
python manage.py createsuperuser
```
- Staff Users: Add staff users through the admin panel. When selecting their role, they will automatically be assigned to the correct group with the appropriate permissions.
- Customers: Customers can register directly through the application’s registration page. They will automatically be assigned to the "Customer" group.

### **7. Run the Server**
```
python manage.py runserver
```

## 🌟 Bonuses

- **Testing**: Comprehensive unit and integration tests are implemented, particularly covering order-related views and functionality.
- **Asynchronous Views**:
  - Implements an asynchronous REST API view, `related_products`, that fetches and returns related product data as JSON.
  - Uses Django's async capabilities and integrates with JavaScript for a seamless user experience.
- **Django REST Capabilities**: Added REST API functionality through the `ContactMessageApiView`, allowing users to submit contact messages with proper validation and response handling.
- **Extended Django User Model**: The Django user model has been extended to include additional fields (e.g., `role`, `slug`) and linked with a one-to-one Profile model for enhanced customization.
- **Deployment**: The application is deployed to Azure, with a live link provided in the README for easy access.

### 🛠️ Additional Functionality

- **Media Storage**: Integrated Cloudinary for efficient and secure media storage and retrieval.
- **Signals**:
  - Automatically create a profile when a user is created.
  - Sync `is_active` status on profile deactivation.
  - Assign groups and permissions to users on creation based on roles.
  - Clean up Cloudinary images when products are deleted.
- **Content Type Framework**: Utilized to manage product relationships dynamically.
- **Context Processors**: Shared context (e.g., cart item count) across templates to simplify logic and improve usability.
- **Group Permissions**:
  - **Admin Panel Permissions**: Group permissions for the admin panel are assigned automatically based on roles.
  - **Frontend Permissions**: These are managed separately using custom permission mixins.


## 📋 General Requirements

- **Implemented using Django Framework** with PostgreSQL as the database service.
- Combines **Function-Based Views (FBV)** and **Class-Based Views (CBV)**, leveraging Django's generic CBVs extensively.
- Includes **more than 10 web pages** and **5+ templates**, ensuring proper use of template inheritance for code reusability.
- Extends the Django User model with a **Profile model** (1-to-1 relation) for additional fields beyond authentication.
- Implements other domain-specific models such as **Plant, Gift, Order, OrderItem, and ContactMessage**.
- Provides **5+ forms**, ensuring proper field validation and error messages for a good UX.
- Uses Django Template Engine with additional **JavaScript** for specific interactive features.
- Designed with **Bootstrap** and customized using **Sass** for styling. The design is fully responsive for improved UX.
- Implements **login/register/logout functionality**:
  - **Public pages** include: Landing page, lists (e.g., plants, gifts), detail pages, Contact Us, and a "Coming Soon" events page.
  - **Private pages** include: Admin and staff-specific stock management pages, profile management pages, shopping cart, and checkout.
- **Customized Admin Site**:
  - Superusers have **full CRUD functionalities**.
  - Staff have **restricted CRUD functionalities** (managed through roles and signals).
- Prevents unauthorized actions like deleting products tied to pending orders, or users tied to orders, etc.
- **Comprehensive exception handling and data validation**:
  - Validations occur at multiple levels (models, forms, admin, and views).
  - Appropriate error messages for invalid inputs.
- **Manages security**:
  - Prevents XSS, CSRF, and other vulnerabilities using Django's built-in mechanisms.
  - Makes use of uniquely generated slugs in URL patterns instead of exposing user IDs.
- Adheres to OOP principles like **inheritance** and **abstraction**.
- Ensures **strong cohesion** through well-defined roles of classes, models, views, etc., and **loose coupling** through the use of mixins and abstraction.

## 🏷️ Credits

Original image names from Unsplash are documented in the file `unsplash_original_image_references.xlsx`.


