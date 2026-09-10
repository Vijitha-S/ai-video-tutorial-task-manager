CREATE DATABASE IF NOT EXISTS ai_video_task_manager;

USE ai_video_task_manager;


-- 1. USER TABLE
CREATE TABLE IF NOT EXISTS USER_TABLE (
    username VARCHAR(50) PRIMARY KEY,
    password VARCHAR(255) NOT NULL
);


-- 2. TASK ITEM TABLE
CREATE TABLE IF NOT EXISTS TASK_ITEM_TABLE (
    task_item_id VARCHAR(100) PRIMARY KEY,
    lesson_id VARCHAR(100) NOT NULL,
    assigned_to VARCHAR(100) NOT NULL,
    start_date DATE NOT NULL,
    due_date DATE NOT NULL,
    status VARCHAR(30) NOT NULL
);


-- 3. TASK STAGE TABLE
CREATE TABLE IF NOT EXISTS TASK_STAGE_TABLE (
    stage_id INT PRIMARY KEY AUTO_INCREMENT,
    task_item_id INT NOT NULL,
    stage_name VARCHAR(100) NOT NULL,
    stage_status VARCHAR(30) NOT NULL,
    last_updated_date DATE NOT NULL,
    status VARCHAR(30) NOT NULL,

    FOREIGN KEY (task_item_id)
        REFERENCES TASK_ITEM_TABLE(task_item_id)
        ON DELETE CASCADE
);


-- 4. REMINDER LOG TABLE
CREATE TABLE IF NOT EXISTS REMINDER_LOG (
    reminder_id INT PRIMARY KEY AUTO_INCREMENT,
    task_item_id VARCHAR(100) NOT NULL,
    lesson_id VARCHAR(100) NOT NULL,
    reminder_type VARCHAR(30) NOT NULL,
    reminder_date DATETIME DEFAULT CURRENT_TIMESTAMP
);


-- SAMPLE USER
INSERT INTO USER_TABLE (username, password)
VALUES ('admin', 'admin123');


-- SAMPLE TASK
INSERT INTO TASK_ITEM_TABLE
(lesson_id, assigned_to, start_date, due_date, status)
VALUES
(
    'AI-AGENT-001',
    'Vijitha',
    '2026-09-01',
    '2026-09-04',
    'Not Completed'
);


-- SAMPLE WORKFLOW STAGES
INSERT INTO TASK_STAGE_TABLE
(task_item_id, stage_name, stage_status, last_updated_date, status)
VALUES
(1, 'AI Image Creation', 'Completed', '2026-09-01', 'Completed'),
(1, 'Image Voice-over', 'Completed', '2026-09-01', 'Completed'),
(1, 'Screen Recording', 'Pending', '2026-09-03', 'Not Completed'),
(1, 'Screen Recording Voice-over', 'Pending', '2026-09-03', 'Not Completed'),
(1, 'Video Editing', 'Pending', '2026-09-03', 'Not Completed');