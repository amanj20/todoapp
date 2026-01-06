import os
from flask import Flask, request, redirect, render_template, abort
from dotenv import load_dotenv
from db import init_db, connect

MAX_TITLE_LEN = 120


def create_app():
    load_dotenv()  # loads .env if you create one later (optional)

    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-only-change-me")

    # Initialize DB on app startup (Flask 3 compatible)
    init_db()

    @app.get("/")
    def index():
        with connect() as conn:
            tasks = conn.execute(
                "SELECT id, title, done FROM tasks ORDER BY id DESC"
            ).fetchall()
        return render_template("index.html", tasks=tasks)

    @app.post("/tasks")
    def add_task():
        title = (request.form.get("title") or "").strip()
        if not title or len(title) > MAX_TITLE_LEN:
            abort(400, "Invalid title")

        with connect() as conn:
            conn.execute(
                "INSERT INTO tasks(title, done) VALUES(?, ?)",
                (title, 0),
            )
            conn.commit()

        return redirect("/")

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

        return redirect("/")

    @app.post("/tasks/<int:task_id>/delete")
    def delete_task(task_id: int):
        with connect() as conn:
            conn.execute(
                "DELETE FROM tasks WHERE id = ?",
                (task_id,),
            )
            conn.commit()

        return redirect("/")

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
