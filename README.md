# 🎬 AI Video Tutorial Task Management System

A professional web-based **AI Video Tutorial Task Management System** designed to manage, monitor, and track the complete workflow of creating AI-powered video tutorials.

The application helps users manage tutorial tasks, track workflow stages, monitor deadlines, generate reports, and maintain reminder logs for overdue work.

## 🚀 Project Overview

Creating an AI video tutorial involves multiple stages such as image creation, voice-over preparation, screen recording, and video editing. Managing these activities manually can make it difficult to track progress and identify delayed tasks.

This system provides a centralized platform to:

* Create and manage tutorial tasks
* Assign tasks to users
* Track task deadlines and completion status
* Monitor individual workflow stages
* Identify overdue tasks
* Generate task and stage reports
* Apply automated reminder rules
* Maintain reminder history
* Provide a clean and professional management interface

## ✨ Key Features

### 🔐 User Authentication

* Username and password-based login
* Session-based authentication
* Logout functionality
* Forgot Password functionality
* Username/password management

### 📋 Task Item Management

* Add new tutorial tasks
* Update existing tasks
* Delete tasks
* Search and filter tasks
* Track Task ID, Lesson ID, Assigned User, Start Date, Due Date, and Status

### 🔄 Task Stage Management

Each tutorial task follows exactly **5 workflow stages**:

1. AI Image Creation
2. Image Voice-over
3. Screen Recording
4. Screen Recording Voice-over
5. Video Editing

Each stage maintains its own status and last-updated date.

### 📊 Reporting Dashboard

The report section provides:

* Total task count
* Completed task count
* Pending task count
* Total workflow stages
* Completed stages
* Pending stages
* Stage-level progress
* Due-date monitoring
* Overdue-day calculation
* Reminder action information

### 🔔 Reminder Management

The system applies the following reminder policy:

* **1+ day overdue → Email**
* **2+ days overdue → WhatsApp**
* **5+ days overdue → IVR**

Reminder actions are recorded in the `REMINDER_LOG` table.

Duplicate reminder entries are prevented for the same task, reminder type, and day.

> Note: The current implementation records reminder actions; it does not actually send Email, WhatsApp, or IVR messages.

## 🗄️ Database

The application uses **MySQL**.

Main database tables:

* `USER_TABLE` – Stores login credentials
* `TASK_ITEM_TABLE` – Stores tutorial task information
* `TASK_STAGE_TABLE` – Stores workflow stage information
* `REMINDER_LOG` – Stores reminder records

The database structure and sample data are provided in `database.sql`.

## 🛠️ Technology Stack

### Backend

* Python
* FastAPI
* Uvicorn
* Jinja2

### Frontend

* HTML5
* CSS3
* Jinja2 Templates

### Database

* MySQL
* MySQL Connector/Python

### Other

* Python-dotenv
* Starlette Session Middleware

## 📁 Project Structure

```text
AI-Video-Tutorial-Task-Management-System/
│
├── main.py
├── database.py
├── database.sql
├── requirements.txt
├── README.md
│
├── templates/
│   ├── login.html
│   ├── menu.html
│   ├── task_items.html
│   ├── task_stage.html
│   └── report.html
│
└── static/
    └── style.css
```

### 📄 Important Files

* `main.py` – Main FastAPI application, routes, authentication, task management, stage management, reports, and reminder logic
* `database.py` – MySQL connection and database utilities
* `database.sql` – Database schema and sample data
* `requirements.txt` – Required Python packages
* `templates/` – Application HTML pages
* `static/style.css` – Application styling
* `README.md` – Project documentation

## ⚙️ How to Run

### 1️⃣ Install Python

Make sure Python is installed on your system.

Check the installation:

```bash
python --version
```

### 2️⃣ Install MySQL

Install and start MySQL Server.

Create the required database and tables using the provided:

`database.sql`

### 3️⃣ Configure Database

Update the database connection details in `database.py` according to your MySQL configuration.

### 4️⃣ Install Dependencies

Open the project folder in a terminal and run:

```bash
pip install -r requirements.txt
```

### 5️⃣ Start the FastAPI Application

Run:

```bash
uvicorn main:app --reload
```

### 6️⃣ Open the Application

Open the displayed local URL in your browser, normally:

```text
http://127.0.0.1:8000
```

### 7️⃣ API Documentation

FastAPI interactive documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## 🔄 Application Workflow

**Login → Main Menu → Task Items / Task Stage / Report**

### Task Workflow

**Create Task → Automatically Create 5 Stages → Update Stage Progress → Monitor Report → Check Overdue Tasks → Generate Reminder Logs**

## 📌 Main Routes

| Route            | Purpose                   |
| ---------------- | ------------------------- |
| `/`              | Login page                |
| `/login`         | User authentication       |
| `/logout`        | Logout                    |
| `/menu`          | Main menu                 |
| `/task-items`    | Task management           |
| `/tasks`         | Task API                  |
| `/task-stage`    | Workflow stage management |
| `/report`        | Reports and monitoring    |
| `/reminder-logs` | Reminder history          |
| `/run-reminders` | Execute reminder checking |
| `/database-test` | Test database connection  |
| `/docs`          | FastAPI API documentation |

## 🔔 Reminder Logic

The system identifies overdue and incomplete tasks based on the task due date.

| Overdue Period | Reminder |
| -------------- | -------- |
| 1+ day         | Email    |
| 2+ days        | WhatsApp |
| 5+ days        | IVR      |

The system also prevents duplicate reminder records for the same task, reminder type, and date.

## 🎯 Project Objective

The objective of this project is to provide a structured and efficient solution for managing AI video tutorial production activities while demonstrating practical implementation of:

* Web application development
* FastAPI backend development
* MySQL database management
* CRUD operations
* User authentication
* Workflow management
* Deadline monitoring
* Automated reminder logic
* Reporting and monitoring

## 👩‍💻 Developed By

**Vijitha S**

BCA Graduate | Python | FastAPI | AI/GenAI | SQL | Web Development

## 📄 License

This project was developed as part of an **Internship Application Development Task**.
