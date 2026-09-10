# 🎬 AI Video Tutorial Task Management System

A professional web-based **AI Video Tutorial Task Management System** designed to manage, monitor, and track the complete workflow of creating AI-powered video tutorials.

The application helps users manage tutorial tasks, track individual workflow stages, monitor deadlines, generate reports, and maintain reminder logs for overdue work.

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
* Maintain a reminder history/log
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
* Track:

  * Task ID
  * Lesson ID
  * Assigned user
  * Start date
  * Due date
  * Status

### 🔄 Task Stage Management

Each tutorial task follows a defined workflow:

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
* Stage-level progress information
* Due-date monitoring
* Overdue-day calculation

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
* `REMINDER_LOG` – Stores generated reminder records

The complete database structure and sample data are provided in `database.sql`.

## 🛠️ Technology Stack

**Backend**

* Python
* FastAPI
* Uvicorn

**Frontend**

* HTML5
* CSS3
* Jinja2 Templates

**Database**

* MySQL
* MySQL Connector/Python

**Other**

* Python-dotenv
* Starlette Session Middleware

## 📁 Project Structure

`main.py` – FastAPI application and backend routes
`database.py` – Database connection and database utilities
`database.sql` – Database schema and sample data
`requirements.txt` – Python dependencies
`README.md` – Project documentation
`templates/` – HTML pages
`static/` – CSS and frontend assets

## 🔄 Application Workflow

**Login → Main Menu → Task Items / Task Stage / Report**

Task Items are created and automatically associated with the predefined workflow stages.

As stages are updated, the system reflects their current progress in the reporting section.

When tasks become overdue, the reminder logic determines the appropriate reminder levels and records them in the reminder log.

## 📌 Main Routes

* `/` – Login
* `/login` – User login
* `/logout` – Logout
* `/menu` – Main menu
* `/task-items` – Task management
* `/task-stage` – Workflow stage management
* `/report` – Reports and monitoring
* `/reminder-logs` – Reminder history
* `/run-reminders` – Execute reminder checking
* `/database-test` – Database connection test

## 🔒 Security Note

Sensitive credentials should not be committed to GitHub.

Use environment variables for database configuration and keep `.env` out of the repository.

## 🎯 Project Objective

The objective of this project is to provide a structured and efficient solution for managing AI video tutorial production activities while demonstrating practical implementation of:

* Web application development
* REST API development
* Database management
* CRUD operations
* Authentication
* Workflow management
* Deadline monitoring
* Automated reminder logic
* Reporting and data visualization

## 👩‍💻 Developed By

**Vijitha S**

BCA Graduate | Python | FastAPI | AI/GenAI | SQL | Web Development

## 📄 License

This project was developed as part of an **internship application development task**.
