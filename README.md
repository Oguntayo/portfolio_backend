## **Portfolio Backend** 🚀  
Django REST API for my portfolio project, featuring authentication, project management, and blog functionalities.  

### **🔧 Features**  
✅ JWT authentication with Django REST Framework (DRF)  
✅ CRUD APIs for projects and blogs  
✅ PostgreSQL database (Hosted on Railway)  
✅ Swagger API documentation  
✅ Deployed on Render with CI/CD  

### **📌 Setup Guide (Local Development)**  

#### **1️⃣ Clone the Repository**  
```bash
git clone https://github.com/Oguntayo/portfolio_backend.git
cd portfolio_backend
```

#### **2️⃣ Create & Activate Virtual Environment**  
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### **3️⃣ Install Dependencies**  
```bash
pip install -r requirements.txt
```

#### **4️⃣ Configure Environment Variables**  
Copy the example environment file and update your credentials:
```bash
cp env_sample .env
```
Edit the `.env` file and update your database settings and secrets accordingly.

#### **5️⃣ Run Migrations**  
```bash
python manage.py migrate
```

#### **6️⃣ Create a Superuser (Optional, for Admin Access)**  
```bash
python manage.py createsuperuser
```

#### **7️⃣ Start the Development Server**  
```bash
python manage.py runserver
```
Your API will be available at **`http://127.0.0.1:8000/`**  

---

### **📖 API Documentation**  
Swagger UI: **`http://127.0.0.1:8000/swagger/`**  

### **🛠️ Technologies Used**  
- Django & Django REST Framework  
- PostgreSQL  
- Simple JWT for authentication  
- Railway (Database hosting)  
- Render (Deployment)  

---

