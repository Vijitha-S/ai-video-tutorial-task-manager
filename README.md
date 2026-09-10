# AI Video Tutorial Task Management System

## 1. Project Overview

The **AI Video Tutorial Task Management System** is a web-based application developed to manage and monitor the workflow involved in creating AI-based educational video tutorials.

The system allows users to:

- Log in securely to the application
- Create and manage tutorial tasks
- Track workflow stages for each task
- Update task and stage statuses
- Search and manage task records
- View task and stage progress
- Generate task and stage reports
- Identify overdue stages
- Apply reminder rules based on overdue duration
- Maintain a reminder history in the database

---

## 2. Technology Stack

### Backend
- Python
- FastAPI
- Uvicorn

### Frontend
- HTML5
- CSS3
- Jinja2 Templates

### Database
- MySQL
- MySQL Connector for Python

### Other
- Starlette Session Middleware
- Python Multipart
- Environment variables using `.env`

---

## 3. Main Features

### Login

The application provides a login system using a username and password stored in the MySQL database.

After successful login, the user is redirected to the main menu.

---

### Main Menu

The main menu provides navigation to:

1. Task Items
2. Task Stage
3. Report

---

### Task Items

The Task Items module allows users to:

- View all tutorial tasks
- Search tasks
- Add a new task
- Update an existing task
- Delete a task
- View individual task information

Each task contains:

- Task Item ID
- Lesson ID
- Assigned To
- Start Date
- Due Date
- Status

When a new task is created, the system automatically creates the required workflow stages.

---

### Task Stage

The Task Stage module is used to track the workflow stages of tutorial production.

The application uses five workflow stages:

1. AI Image Creation
2. Image Voice-over
3. Screen Recording
4. Screen Recording Voice-over
5. Video Editing

Each stage contains:

- Stage ID
- Task Item ID
- Stage Name
- Stage Status
- Last Updated Date
- Status

Stage statuses can be:

- Pending
- In Progress
- Completed

Users can update the stage information through the Task Stage interface.

---

## 4. Reporting

The Report module provides an overview of task and stage progress.

### Task Summary

The report displays:

- Total Tasks
- Completed Tasks
- Pending Tasks

### Stage Summary

The report displays:

- Total Stages
- Completed Stages
- Pending Stages

### Stage Report

The report also provides detailed information about each workflow stage, including:

- Task Stage ID
- Task Item ID
- Lesson ID
- Stage Name
- Stage Status
- Last Updated Date
- Status
- Due Date

---

## 5. Overdue Detection

The application checks the due date of incomplete stages.

If a stage is incomplete and its task due date has passed, the system calculates the number of overdue days.

The report displays statuses such as:

- On Time
- Completed
- 1 Day Overdue
- 2 Days Overdue
- 5 Days Overdue

and other corresponding overdue durations.

---

## 6. Reminder System

The application includes a reminder workflow for overdue tasks.

The reminder policy is:

| Overdue Duration | Reminder |
|---|---|
| 1+ Day | Email |
| 2+ Days | WhatsApp |
| 5+ Days | IVR |

The system currently **logs reminder actions** rather than actually sending external Email, WhatsApp, or IVR messages.

---

## 7. Reminder Log

The `REMINDER_LOG` table stores reminder history.

Each reminder record contains:

- Reminder ID
- Task Item ID
- Lesson ID
- Reminder Type
- Reminder Date

The system prevents the same reminder type from being logged more than once for the same task on the same day.

The reminder log can be checked through:

```text
GET /reminder-logs