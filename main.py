from dataclasses import dataclass
from flask import Flask, render_template, request, url_for, flash
from werkzeug.utils import redirect

app = Flask(__name__)
app.config.update(
    SECRET_KEY="ytfhgjhjhjhjh465765"
)


@dataclass
class TodoItem:
    text: str
    done: bool = False


todos = [
    TodoItem("Learn Flask"),
    TodoItem("Learn FastAPI"),
    TodoItem("Learn Django"),
]


@app.get("/", endpoint="todos-list")
def todo_list():
    return render_template("index.html", todos=todos)

@app.post("/")
def todo_add():
    text = request.form.get("todo-text")
    if text:
        todos.append(
            TodoItem(text)
        )
    else:
        flash("error, text not passed")
    return redirect(url_for("todos-list"))


if __name__ == '__main__':
    app.run(debug=True)