# 📝 Flask Blogify

A complete blog platform built with **Flask**, **MySQL**, and **Jinja2**. This app supports **user signup/login**, **post creation**, **editing**, **deleting**, and includes a **contact form** that emails the admin.

---

## 🚀 Features

- 🔐 Secure User Signup & Login with session management
- 📝 Create, Edit, and Delete blog posts
- 📰 View all posts or filter user-specific posts
- 👤 View profile with username and email
- 📬 Contact form that sends admin an email using Gmail SMTP
- 🌐 Responsive HTML templates using Jinja2 & Bootstrap
- 🗃️ MySQL database integration using SQLAlchemy ORM

---

## 📁 Project Structure

```
BLOG_APP/
├── static/                   # CSS, images
│   ├── style.css
│   ├── profile.css
│   ├── bapp.jpg
│   └── mbgimg.jpg
│
├── templates/                # HTML templates
│   ├── layout.html
│   ├── home.html
│   ├── login.html
│   ├── signup.html
│   ├── profile.html
│   ├── create.html
│   ├── edit.html
│   ├── posts.html
│   ├── contact.html
│   ├── my_blogs.html
│   ├── specific_post.html    
│   └── sample_config.json
│
├── venv/                     # Python virtual environment (excluded)
├── app.py                    # Main Flask application
├── create_db.py              # Script to auto-create database tables
├── .gitignore                # Git ignore file
```

---

## Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/blogify.git
cd blogify
```

### 2️⃣ Create & Activate Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate        # On Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Setup Configuration

Inside the `templates/` folder:

- Rename `sample_config.json` ➡️ `config.json`
- Fill in your actual values:

```json
{
  "params": {
    "database_uri": "mysql+pymysql://root:password@localhost/blogify",
    "gmail-user": "your-email@gmail.com",
    "gmail-pass": "your-password",
    "app.secret_key": "your-secret-key"
  }
}
```

### 5️⃣ Initialize the Database

```bash
python create_db.py
```

This will auto-create required tables using SQLAlchemy.

### 6️⃣ Run the Flask App

```bash
python app.py
```

Now visit `http://127.0.0.1:5000/` in your browser.

---

## 📷 Key Screens

- ✅ Login & Signup Page
- ✅ Create Blog Form
- ✅ User Profile View
- ✅ Home Feed with Latest Posts
- ✅ Post Details
- ✅ Contact Form



## 📄 License

```
Free to use, modify, and share — with credits!

---

