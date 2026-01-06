import os
from flask import Flask, request, redirect, render_template, abort
from dotenv import load_dotenv
from db import init_db, connect

MAX_TITLE_LEN = 120

def create_app():
    load_dotenv()  

    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-only-change-me")

    init_db()

    def _counts(conn):
        total = conn.execute("SELECT COUNT(*) AS c FROM tasks").fetchone()["c"]
        completed = conn.execute("SELECT COUNT(*) AS c FROM tasks WHERE done = 1").fetchone()["c"]
        active = total - completed
        return total, active, completed

    @app.get("/")
    def index():
        f = (request.args.get("filter") or "all").lower()
        if f not in {"all", "active", "completed"}:
            f = "all"

        where = ""
        if f == "active":
            where = "WHERE done = 0"
        elif f == "completed":
            where = "WHERE done = 1"

        with connect() as conn:
            total, active, completed = _counts(conn)
            tasks = conn.execute(
                f"SELECT id, title, done, created_at FROM tasks {where} ORDER BY id DESC"
            ).fetchall()

        return render_template(
            "index.html",
            tasks=tasks,
            filter=f,
            total=total,
            active=active,
            completed=completed
        )

    @app.post("/tasks")
    def add_task():
        title = (request.form.get("title") or "").strip()
        if not title or len(title) > MAX_TITLE_LEN:
            abort(400, "Invalid title")

        with connect() as conn:
            conn.execute(
                "INSERT INTO tasks(title, done, created_at) VALUES(?, ?, CURRENT_TIMESTAMP)",
                (title, 0),
            )
            conn.commit()

        return redirect(request.referrer or "/")

    @app.post("/tasks/<int:task_id>/toggle")
    def toggle_task(task_id: int):
        with connect() as conn:
            row = conn.execute(
                "SELECT done FROM tasks WHERE id = ?",
                (task_id,),
            ).fetchone()

            if not row:
                abort(404)

            new_done = 0 if row["done"] else 1
            conn.execute(
                "UPDATE tasks SET done = ? WHERE id = ?",
                (new_done, task_id),
            )
            conn.commit()

        return redirect(request.referrer or "/")

    @app.post("/tasks/<int:task_id>/edit")
    def edit_task(task_id: int):
        title = (request.form.get("title") or "").strip()
        if not title or len(title) > MAX_TITLE_LEN:
            abort(400, "Invalid title")

        with connect() as conn:
            cur = conn.execute(
                "UPDATE tasks SET title = ? WHERE id = ?",
                (title, task_id),
            )
            conn.commit()

            if cur.rowcount == 0:
                abort(404)

        return redirect(request.referrer or "/")

    @app.post("/tasks/<int:task_id>/delete")
    def delete_task(task_id: int):
        with connect() as conn:
            conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()
        return redirect(request.referrer or "/")

    @app.post("/tasks/clear")
    def clear_tasks():
        with connect() as conn:
            conn.execute("DELETE FROM tasks")
            conn.commit()
        return redirect("/")

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
