from datetime import date, datetime
from fastapi import FastAPI, HTTPException, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from database import get_connection


# ============================================================
# APP
# ============================================================

app = FastAPI(
    title="AI Video Tutorial Task Management System",
    version="3.0.0"
)

app.add_middleware(
    SessionMiddleware,
    secret_key="ai-video-task-manager-secret-key"
)

templates = Jinja2Templates(directory="templates")


# ============================================================
# WORKFLOW STAGES
# ============================================================

STAGES = [
    "AI Image Creation",
    "Image Voice-over",
    "Screen Recording",
    "Screen Recording Voice-over",
    "Video Editing"
]


# ============================================================
# DATABASE HELPER
# ============================================================

def close_connection(connection, cursor):
    try:
        if cursor:
            cursor.close()
    except Exception:
        pass

    try:
        if connection:
            connection.close()
    except Exception:
        pass


# ============================================================
# LOGIN
# ============================================================

@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "request": request,
            "error": request.query_params.get("error"),
            "message": request.query_params.get("message")
        }
    )


@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "request": request,
            "error": request.query_params.get("error"),
            "message": request.query_params.get("message")
        }
    )


# ============================================================
# LOGIN AUTHENTICATION
# IMPORTANT: Login always checks the CURRENT values stored in
# USER_TABLE. Therefore, changing the password below immediately
# changes the password used by the login route.
# ============================================================

@app.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    connection = None
    cursor = None

    username = username.strip()

    if not username or not password:
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={
                "request": request,
                "error": "Username and password are required",
                "message": None
            },
            status_code=400
        )

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        # USER_TABLE contains the active login credentials.
        # This query does NOT use hard-coded credentials.
        cursor.execute(
            """
            SELECT username
            FROM USER_TABLE
            WHERE username = %s
              AND password = %s
            LIMIT 1
            """,
            (username, password)
        )

        user = cursor.fetchone()

        if not user:
            return templates.TemplateResponse(
                request=request,
                name="login.html",
                context={
                    "request": request,
                    "error": "Invalid username or password",
                    "message": None
                },
                status_code=401
            )

        # Store the CURRENT username in the session.
        request.session["username"] = user["username"]

        return RedirectResponse(
            url="/menu",
            status_code=303
        )

    except Exception as e:
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={
                "request": request,
                "error": f"Login failed: {str(e)}",
                "message": None
            },
            status_code=500
        )

    finally:
        close_connection(connection, cursor)


# ============================================================
# FORGOT PASSWORD
# ============================================================
# This is a simple local/demo recovery flow suitable for this
# internship project. It verifies that the username exists and
# then updates the password in USER_TABLE.
# ============================================================

@app.get("/forgot-password", response_class=HTMLResponse)
def forgot_password_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="forgot_password.html",
        context={
            "request": request,
            "error": None,
            "message": None
        }
    )


@app.post("/forgot-password")
def forgot_password(
    request: Request,
    username: str = Form(...),
    new_password: str = Form(...),
    confirm_password: str = Form(...)
):
    connection = None
    cursor = None

    username = username.strip()

    if not username or not new_password or not confirm_password:
        return templates.TemplateResponse(
            request=request,
            name="forgot_password.html",
            context={
                "request": request,
                "error": "All fields are required",
                "message": None
            },
            status_code=400
        )

    if new_password != confirm_password:
        return templates.TemplateResponse(
            request=request,
            name="forgot_password.html",
            context={
                "request": request,
                "error": "New passwords do not match",
                "message": None
            },
            status_code=400
        )

    if len(new_password) < 6:
        return templates.TemplateResponse(
            request=request,
            name="forgot_password.html",
            context={
                "request": request,
                "error": "Password must contain at least 6 characters",
                "message": None
            },
            status_code=400
        )

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        # First verify that the username exists.
        cursor.execute(
            """
            SELECT username
            FROM USER_TABLE
            WHERE username = %s
            LIMIT 1
            """,
            (username,)
        )

        user = cursor.fetchone()

        if not user:
            return templates.TemplateResponse(
                request=request,
                name="forgot_password.html",
                context={
                    "request": request,
                    "error": "Username not found",
                    "message": None
                },
                status_code=404
            )

        # Update the password in the same table used by /login.
        cursor.execute(
            """
            UPDATE USER_TABLE
            SET password = %s
            WHERE username = %s
            """,
            (new_password, username)
        )

        connection.commit()

        return RedirectResponse(
            url="/login?message=Password reset successfully. You can now sign in with your new password.",
            status_code=303
        )

    except Exception as e:
        if connection:
            connection.rollback()

        return templates.TemplateResponse(
            request=request,
            name="forgot_password.html",
            context={
                "request": request,
                "error": f"Password reset failed: {str(e)}",
                "message": None
            },
            status_code=500
        )

    finally:
        close_connection(connection, cursor)


# ============================================================
# CHANGE USERNAME / PASSWORD
# ============================================================
# This page is available only after successful login.
# The current password is required before credentials can be
# changed. After a successful update, the session is updated to
# the new username automatically.
# ============================================================

@app.get("/change-credentials", response_class=HTMLResponse)
def change_credentials_page(request: Request):
    current_username = request.session.get("username")

    if not current_username:
        return RedirectResponse(
            url="/login?error=Please sign in first",
            status_code=303
        )

    return templates.TemplateResponse(
        request=request,
        name="change_credentials.html",
        context={
            "request": request,
            "current_username": current_username,
            "error": None,
            "message": None
        }
    )


@app.post("/change-credentials")
def change_credentials(
    request: Request,
    current_password: str = Form(...),
    new_username: str = Form(...),
    new_password: str = Form(...),
    confirm_password: str = Form(...)
):
    current_username = request.session.get("username")

    if not current_username:
        return RedirectResponse(
            url="/login?error=Your session has expired. Please sign in again.",
            status_code=303
        )

    connection = None
    cursor = None

    new_username = new_username.strip()

    if not current_password or not new_username or not new_password or not confirm_password:
        return templates.TemplateResponse(
            request=request,
            name="change_credentials.html",
            context={
                "request": request,
                "current_username": current_username,
                "error": "All fields are required",
                "message": None
            },
            status_code=400
        )

    if new_password != confirm_password:
        return templates.TemplateResponse(
            request=request,
            name="change_credentials.html",
            context={
                "request": request,
                "current_username": current_username,
                "error": "New passwords do not match",
                "message": None
            },
            status_code=400
        )

    if len(new_password) < 6:
        return templates.TemplateResponse(
            request=request,
            name="change_credentials.html",
            context={
                "request": request,
                "current_username": current_username,
                "error": "Password must contain at least 6 characters",
                "message": None
            },
            status_code=400
        )

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        # Verify the CURRENT password before making any change.
        cursor.execute(
            """
            SELECT username
            FROM USER_TABLE
            WHERE username = %s
              AND password = %s
            LIMIT 1
            """,
            (current_username, current_password)
        )

        current_user = cursor.fetchone()

        if not current_user:
            return templates.TemplateResponse(
                request=request,
                name="change_credentials.html",
                context={
                    "request": request,
                    "current_username": current_username,
                    "error": "Current password is incorrect",
                    "message": None
                },
                status_code=401
            )

        # If the username is being changed, make sure another user
        # does not already have the requested username.
        cursor.execute(
            """
            SELECT username
            FROM USER_TABLE
            WHERE username = %s
              AND username <> %s
            LIMIT 1
            """,
            (new_username, current_username)
        )

        existing_user = cursor.fetchone()

        if existing_user:
            return templates.TemplateResponse(
                request=request,
                name="change_credentials.html",
                context={
                    "request": request,
                    "current_username": current_username,
                    "error": "That username is already in use",
                    "message": None
                },
                status_code=409
            )

        # IMPORTANT: update BOTH username and password in USER_TABLE.
        # The /login route above reads the same columns, so the new
        # credentials become active immediately after this commit.
        cursor.execute(
            """
            UPDATE USER_TABLE
            SET username = %s,
                password = %s
            WHERE username = %s
            """,
            (new_username, new_password, current_username)
        )

        connection.commit()

        # Keep the logged-in session synchronized with the new username.
        request.session["username"] = new_username

        return RedirectResponse(
            url="/menu?message=Login credentials updated successfully",
            status_code=303
        )

    except Exception as e:
        if connection:
            connection.rollback()

        return templates.TemplateResponse(
            request=request,
            name="change_credentials.html",
            context={
                "request": request,
                "current_username": current_username,
                "error": f"Credential update failed: {str(e)}",
                "message": None
            },
            status_code=500
        )

    finally:
        close_connection(connection, cursor)


@app.get("/logout")
def logout(request: Request):
    request.session.clear()

    return RedirectResponse(
        url="/",
        status_code=303
    )


# ============================================================
# MAIN MENU
# ============================================================

@app.get("/menu", response_class=HTMLResponse)
@app.get("/main-menu", response_class=HTMLResponse)
def main_menu(request: Request):

    username = request.session.get("username")

    if not username:
        return RedirectResponse(
            url="/",
            status_code=303
        )

    return templates.TemplateResponse(
        request=request,
        name="menu.html",
        context={
            "request": request,
            "username": username,
            "message": request.query_params.get("message"),
            "error": request.query_params.get("error")
        }
    )


# ============================================================
# DATABASE TEST
# ============================================================

@app.get("/database-test")
def database_test():

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT DATABASE()")
        result = cursor.fetchone()

        return {
            "status": "connected",
            "message": "Database connection successful",
            "database": result[0]
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database connection failed: {str(e)}"
        )

    finally:
        close_connection(connection, cursor)


# ============================================================
# TASK ITEMS - VIEW + SEARCH
# ============================================================

@app.get("/task-items", response_class=HTMLResponse)
def task_items(
    request: Request,
    search: str = ""
):

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        if search.strip():

            value = f"%{search.strip()}%"

            cursor.execute(
                """
                SELECT
                    task_item_id,
                    lesson_id,
                    assigned_to,
                    start_date,
                    due_date,
                    status
                FROM TASK_ITEM_TABLE
                WHERE
                    task_item_id LIKE %s
                    OR lesson_id LIKE %s
                    OR assigned_to LIKE %s
                    OR status LIKE %s
                ORDER BY task_item_id
                """,
                (
                    value,
                    value,
                    value,
                    value
                )
            )

        else:

            cursor.execute(
                """
                SELECT
                    task_item_id,
                    lesson_id,
                    assigned_to,
                    start_date,
                    due_date,
                    status
                FROM TASK_ITEM_TABLE
                ORDER BY task_item_id
                """
            )

        tasks = cursor.fetchall()

        return templates.TemplateResponse(
            request=request,
            name="task_items.html",
            context={
                "request": request,
                "tasks": tasks,
                "search": search,
                "message": request.query_params.get("message"),
                "error": request.query_params.get("error")
            }
        )

    except Exception as e:

        return templates.TemplateResponse(
            request=request,
            name="task_items.html",
            context={
                "request": request,
                "tasks": [],
                "search": search,
                "message": None,
                "error": f"Failed to load tasks: {str(e)}"
            },
            status_code=500
        )

    finally:
        close_connection(connection, cursor)


# ============================================================
# TASK ITEMS - JSON
# ============================================================

@app.get("/tasks")
def get_all_tasks():

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                task_item_id,
                lesson_id,
                assigned_to,
                start_date,
                due_date,
                status
            FROM TASK_ITEM_TABLE
            ORDER BY task_item_id
            """
        )

        tasks = cursor.fetchall()

        return {
            "status": "success",
            "total_tasks": len(tasks),
            "tasks": tasks
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch tasks: {str(e)}"
        )

    finally:
        close_connection(connection, cursor)


# ============================================================
# TASK ITEM - ADD
# Supports BOTH:
# /task-items/add
# /task-items/create
# ============================================================

@app.post("/task-items/add")
@app.post("/task-items/create")
def create_task(

    task_item_id: str = Form(...),
    lesson_id: str = Form(...),
    assigned_to: str = Form(...),
    start_date: str = Form(...),
    due_date: str = Form(...),
    status: str = Form(...)
):

    connection = None
    cursor = None

    try:

        task_item_id = task_item_id.strip()
        lesson_id = lesson_id.strip()
        assigned_to = assigned_to.strip()
        start_date = start_date.strip()
        due_date = due_date.strip()
        status = status.strip()

        if not task_item_id:
            raise HTTPException(
                status_code=400,
                detail="Task Item ID is required"
            )

        connection = get_connection()
        cursor = connection.cursor()

        # Check duplicate Task ID
        cursor.execute(
            """
            SELECT task_item_id
            FROM TASK_ITEM_TABLE
            WHERE task_item_id = %s
            """,
            (task_item_id,)
        )

        if cursor.fetchone():

            return RedirectResponse(
                url="/task-items?error=Task Item ID already exists",
                status_code=303
            )

        # Create task
        cursor.execute(
            """
            INSERT INTO TASK_ITEM_TABLE
            (
                task_item_id,
                lesson_id,
                assigned_to,
                start_date,
                due_date,
                status
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )
            """,
            (
                task_item_id,
                lesson_id,
                assigned_to,
                start_date,
                due_date,
                status
            )
        )

        # Create exactly 5 workflow stages
        for stage_name in STAGES:

            cursor.execute(
                """
                INSERT INTO TASK_STAGE_TABLE
                (
                    task_item_id,
                    stage_name,
                    stage_status,
                    last_updated_date,
                    status
                )
                VALUES
                (
                    %s,
                    %s,
                    'Pending',
                    CURDATE(),
                    'Not Completed'
                )
                """,
                (
                    task_item_id,
                    stage_name
                )
            )

        connection.commit()

        return RedirectResponse(
            url="/task-items?message=Task added successfully",
            status_code=303
        )

    except HTTPException:
        if connection:
            connection.rollback()
        raise

    except Exception as e:

        if connection:
            connection.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Failed to create task: {str(e)}"
        )

    finally:
        close_connection(connection, cursor)


# ============================================================
# TASK ITEM - UPDATE
# ============================================================

@app.post("/task-items/update")
def update_task(

    task_item_id: str = Form(...),
    lesson_id: str = Form(...),
    assigned_to: str = Form(...),
    start_date: str = Form(...),
    due_date: str = Form(...),
    status: str = Form(...)
):

    connection = None
    cursor = None

    try:

        task_item_id = task_item_id.strip()

        connection = get_connection()
        cursor = connection.cursor()

        # IMPORTANT:
        # task_item_id is VARCHAR, so NEVER convert it to int.
        cursor.execute(
            """
            SELECT task_item_id
            FROM TASK_ITEM_TABLE
            WHERE task_item_id = %s
            """,
            (task_item_id,)
        )

        task = cursor.fetchone()

        if not task:

            return RedirectResponse(
                url="/task-items?error=Task not found",
                status_code=303
            )

        cursor.execute(
            """
            UPDATE TASK_ITEM_TABLE
            SET
                lesson_id = %s,
                assigned_to = %s,
                start_date = %s,
                due_date = %s,
                status = %s
            WHERE task_item_id = %s
            """,
            (
                lesson_id.strip(),
                assigned_to.strip(),
                start_date.strip(),
                due_date.strip(),
                status.strip(),
                task_item_id
            )
        )

        connection.commit()

        return RedirectResponse(
            url="/task-items?message=Task updated successfully",
            status_code=303
        )

    except Exception as e:

        if connection:
            connection.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Failed to update task: {str(e)}"
        )

    finally:
        close_connection(connection, cursor)


# ============================================================
# TASK ITEM - DELETE
# ============================================================

@app.post("/task-items/delete")
def delete_task(
    task_item_id: str = Form(...)
):

    connection = None
    cursor = None

    try:

        task_item_id = task_item_id.strip()

        connection = get_connection()
        cursor = connection.cursor()

        # Check task first
        cursor.execute(
            """
            SELECT task_item_id
            FROM TASK_ITEM_TABLE
            WHERE task_item_id = %s
            """,
            (task_item_id,)
        )

        if not cursor.fetchone():

            return RedirectResponse(
                url="/task-items?error=Task not found",
                status_code=303
            )

        # Delete stages
        cursor.execute(
            """
            DELETE FROM TASK_STAGE_TABLE
            WHERE task_item_id = %s
            """,
            (task_item_id,)
        )

        # Delete task
        cursor.execute(
            """
            DELETE FROM TASK_ITEM_TABLE
            WHERE task_item_id = %s
            """,
            (task_item_id,)
        )

        connection.commit()

        return RedirectResponse(
            url="/task-items?message=Task deleted successfully",
            status_code=303
        )

    except Exception as e:

        if connection:
            connection.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete task: {str(e)}"
        )

    finally:
        close_connection(connection, cursor)


# ============================================================
# SINGLE TASK
# ============================================================

@app.get("/tasks/{task_item_id}")
def get_task(task_item_id: str):

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                task_item_id,
                lesson_id,
                assigned_to,
                start_date,
                due_date,
                status
            FROM TASK_ITEM_TABLE
            WHERE task_item_id = %s
            """,
            (task_item_id.strip(),)
        )

        task = cursor.fetchone()

        if not task:

            raise HTTPException(
                status_code=404,
                detail="Task not found"
            )

        cursor.execute(
            """
            SELECT
                stage_id,
                task_item_id,
                stage_name,
                stage_status,
                last_updated_date,
                status
            FROM TASK_STAGE_TABLE
            WHERE task_item_id = %s
            ORDER BY stage_id
            """,
            (task_item_id.strip(),)
        )

        stages = cursor.fetchall()

        return {
            "status": "success",
            "task": task,
            "stages": stages
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch task: {str(e)}"
        )

    finally:
        close_connection(connection, cursor)


# ============================================================
# TASK STAGE - VIEW + SEARCH
# ============================================================

@app.get("/task-stage", response_class=HTMLResponse)
def task_stage_page(
    request: Request,
    task_item_id: str = ""
):

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        if task_item_id.strip():

            cursor.execute(
                """
                SELECT
                    stage_id,
                    task_item_id,
                    stage_name,
                    stage_status,
                    last_updated_date,
                    status
                FROM TASK_STAGE_TABLE
                WHERE task_item_id = %s
                ORDER BY stage_id
                """,
                (task_item_id.strip(),)
            )

        else:

            cursor.execute(
                """
                SELECT
                    stage_id,
                    task_item_id,
                    stage_name,
                    stage_status,
                    last_updated_date,
                    status
                FROM TASK_STAGE_TABLE
                ORDER BY task_item_id, stage_id
                """
            )

        stages = cursor.fetchall()

        return templates.TemplateResponse(
            request=request,
            name="task_stage.html",
            context={
                "request": request,
                "stages": stages,
                "selected_task": task_item_id,
                "message": request.query_params.get("message"),
                "error": request.query_params.get("error")
            }
        )

    except Exception as e:

        return templates.TemplateResponse(
            request=request,
            name="task_stage.html",
            context={
                "request": request,
                "stages": [],
                "selected_task": task_item_id,
                "message": None,
                "error": f"Failed to load stages: {str(e)}"
            },
            status_code=500
        )

    finally:
        close_connection(connection, cursor)


# ============================================================
# TASK STAGE - UPDATE FROM FORM
# ============================================================

@app.post("/task-stage/update")
def update_task_stage_form(

    stage_id: int = Form(...),
    task_item_id: str = Form(...),
    stage_name: str = Form(...),
    stage_status: str = Form(...),
    last_updated_date: str = Form(...),
    status: str = Form(...)

):

    connection = None
    cursor = None

    try:

        task_item_id = task_item_id.strip()

        connection = get_connection()
        cursor = connection.cursor()

        # Check stage
        cursor.execute(
            """
            SELECT stage_id
            FROM TASK_STAGE_TABLE
            WHERE stage_id = %s
              AND task_item_id = %s
            """,
            (
                stage_id,
                task_item_id
            )
        )

        if not cursor.fetchone():

            return RedirectResponse(
                url=f"/task-stage?error=Stage not found",
                status_code=303
            )

        # Update stage
        cursor.execute(
            """
            UPDATE TASK_STAGE_TABLE
            SET
                stage_name = %s,
                stage_status = %s,
                last_updated_date = %s,
                status = %s
            WHERE
                stage_id = %s
                AND task_item_id = %s
            """,
            (
                stage_name.strip(),
                stage_status.strip(),
                last_updated_date.strip(),
                status.strip(),
                stage_id,
                task_item_id
            )
        )

        connection.commit()

        return RedirectResponse(
            url=f"/task-stage?task_item_id={task_item_id}&message=Stage updated successfully",
            status_code=303
        )

    except Exception as e:

        if connection:
            connection.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Failed to update stage: {str(e)}"
        )

    finally:
        close_connection(connection, cursor)


# ============================================================
# TASK STAGE - API UPDATE
# ============================================================

@app.put("/tasks/{task_item_id}/stages/{stage_id}")
def update_stage(

    task_item_id: str,
    stage_id: int,
    stage_status: str = Form(...),
    status: str = Form(...)

):

    connection = None
    cursor = None

    try:

        task_item_id = task_item_id.strip()

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT stage_id
            FROM TASK_STAGE_TABLE
            WHERE stage_id = %s
              AND task_item_id = %s
            """,
            (
                stage_id,
                task_item_id
            )
        )

        if not cursor.fetchone():

            raise HTTPException(
                status_code=404,
                detail="Stage not found"
            )

        cursor.execute(
            """
            UPDATE TASK_STAGE_TABLE
            SET
                stage_status = %s,
                status = %s,
                last_updated_date = CURDATE()
            WHERE
                stage_id = %s
                AND task_item_id = %s
            """,
            (
                stage_status.strip(),
                status.strip(),
                stage_id,
                task_item_id
            )
        )

        connection.commit()

        return {
            "status": "success",
            "message": "Stage updated successfully",
            "task_item_id": task_item_id,
            "stage_id": stage_id,
            "stage_status": stage_status,
            "task_status": status
        }

    except HTTPException:
        raise

    except Exception as e:

        if connection:
            connection.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Failed to update stage: {str(e)}"
        )

    finally:
        close_connection(connection, cursor)


# ============================================================
# REPORT
# ============================================================

@app.get("/report", response_class=HTMLResponse)
def report_page(request: Request):

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        # ----------------------------------------------------
        # TASK SUMMARY
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT
                COUNT(*) AS total_tasks,

                COALESCE(
                    SUM(
                        CASE
                            WHEN status = 'Completed'
                            THEN 1
                            ELSE 0
                        END
                    ),
                    0
                ) AS completed_tasks,

                COALESCE(
                    SUM(
                        CASE
                            WHEN status != 'Completed'
                            THEN 1
                            ELSE 0
                        END
                    ),
                    0
                ) AS pending_tasks

            FROM TASK_ITEM_TABLE
            """
        )

        task_summary = cursor.fetchone() or {}

        # ----------------------------------------------------
        # STAGE SUMMARY
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT
                COUNT(*) AS total_stages,

                COALESCE(
                    SUM(
                        CASE
                            WHEN stage_status = 'Completed'
                            THEN 1
                            ELSE 0
                        END
                    ),
                    0
                ) AS completed_stages,

                COALESCE(
                    SUM(
                        CASE
                            WHEN stage_status != 'Completed'
                            THEN 1
                            ELSE 0
                        END
                    ),
                    0
                ) AS pending_stages

            FROM TASK_STAGE_TABLE
            """
        )

        stage_summary = cursor.fetchone() or {}

        # ----------------------------------------------------
        # REPORT DATA
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT
                s.stage_id AS TASK_STAGE_ID,
                s.task_item_id AS TASK_ITEM_ID,
                s.stage_name AS STAGE_NAME,
                s.stage_status AS STAGE_STATUS,
                s.last_updated_date AS LAST_UPDATED_DATE,
                s.status AS STATUS,
                t.due_date AS DUE_DATE

            FROM TASK_STAGE_TABLE s

            INNER JOIN TASK_ITEM_TABLE t
                ON s.task_item_id = t.task_item_id

            ORDER BY
                s.task_item_id,
                s.stage_id
            """
        )

        stages = cursor.fetchall()

        # ----------------------------------------------------
        # DUE DATE + REMINDER LOGIC
        # ----------------------------------------------------

        today = date.today()

        for stage in stages:

            due_date = stage.get("DUE_DATE")
            stage_status = stage.get("STAGE_STATUS")
            status = stage.get("STATUS")

            if isinstance(due_date, datetime):
                due_date = due_date.date()

            stage["DUE_STATUS"] = "On Time"
            stage["REMINDER_ACTIONS"] = "No Reminder"

            if (
                stage_status == "Completed"
                or status == "Completed"
            ):

                stage["DUE_STATUS"] = "Completed"

            elif due_date:

                if due_date >= today:

                    stage["DUE_STATUS"] = "On Time"

                else:

                    overdue_days = (today - due_date).days

                    if overdue_days == 1:
                        stage["DUE_STATUS"] = "1 Day Overdue"
                    else:
                        stage["DUE_STATUS"] = (
                            f"{overdue_days} Days Overdue"
                        )

                    actions = []

                    if overdue_days >= 1:
                        actions.append("Email")

                    if overdue_days >= 2:
                        actions.append("WhatsApp")

                    if overdue_days >= 5:
                        actions.append("IVR")

                    if actions:
                        stage["REMINDER_ACTIONS"] = (
                            " → ".join(actions)
                        )

        return templates.TemplateResponse(
            request=request,
            name="report.html",
            context={
                "request": request,
                "task_summary": task_summary,
                "stage_summary": stage_summary,
                "stages": stages,
                "error": None
            }
        )

    except Exception as e:

        return templates.TemplateResponse(
            request=request,
            name="report.html",
            context={
                "request": request,
                "task_summary": {},
                "stage_summary": {},
                "stages": [],
                "error": f"Failed to generate report: {str(e)}"
            },
            status_code=500
        )

    finally:
        close_connection(connection, cursor)