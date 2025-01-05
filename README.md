# Пояснение 
## к приложению To Do List на Flask в рамках дипломной работы студента 
## Абрамова Андрея Васильевича

Используемая литература:
https://flask.palletsprojects.com/en/stable/

Итоговая структура приложения:
![project_tree](https://github.com/andrzejabramov/ToDoList_Flask/blob/master/screens/%20project_tree.png)

Flask - один из трех фреймворков, на которых мы разработаем данное простое приложение для сравнения инструментов разработки Flask, FastAPI, Django.
Для удобства мы инсталлируем и будем использовать библиотеку python Werkzeug: 
```commandline
pip install werkzeug
```
Создаем файл main и и исталлируем Flask:
```commandline
pip install flask
```
Создаем базовые строки кода:
```commandline
from flask import Flask

app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)
```
В корне проекта создаем директорию templates, а в ней файл index.html для вывода результатов в броузер.
Для веб мы будем использовать библтотеку Jinja2.
Наподобие роутов в FastAPI создадим пакет (инициируется наличием файла __init__.py) views для описания логики приложения: добавления записей, удаления или измемения (CRUD).
Эти функции (роуты) с декораторами, содержащими тип запроса и адрес возвращают веб страницу, либо изменяют ее.
Перед описанием функций CRUD мы создадим механизм записи изменений в таблицу, будем использовать SQLite3.
Создадим пакет models, в нем файлы database.py (файл нужен только для того, чтобы из него экспортировать переменную db) и todo_item.py. 
Инсталлируем в виртуальное окружение SQLAlchemy, Flask-SQLAlchemy (надстройка для Flask), Flask-Migrate.
В файле todo_item.py создаем модель таблицы todo_items (класс TodoItem от родителя db.Model).
Подключение к БД создаем в файле config.py
В файле main.py создаем экземпляр класса Migrate и из консоли запускаем инициализацию db:
```commandline
flask db init
```
db берем из файла wsgi.py, который нужен только, чтобы импортировать db, в результате чего появляется директория migrations.
Делаем миграцию:
```commandline
flask db migrate -m "create todos table" 
```
Появляется в папке versions директории migrations файл миграции, проверяем его визуально. В таблице два столбца: имя записи (str) и done (bool) - задание не выпорлнено (по умолчанию) или выполнено.
Далее подключаем наши роуты к БД, чтобы все изменения записывались в таблицу.  
- Роут1 (get) выводит на веб страницу все имеющиеся записи в БД.  
```commandline
@todo_app.get("/", endpoint="list")
def todo_list():
    todos = db.session.query(TodoItem).order_by(TodoItem.id).all()
    #---------------
    return render_template("index.html", todos=todos)
```
- Роут2 (post) добавляет на страницу и в БД запись
```commandline
@todo_app.post("/")
def todo_add():
    text = request.form.get("todo-text")
    if text:
        todo = TodoItem(text=text)
        db.session.add(todo)
        db.session.commit()
    else:
        flash("error, text not passed")
    return redirect(url_for("todo_app.list"))
```
- Роут3 (post) изменяет поле done таблицы Fasle/True и меняет на странице эмодзи, означающие выполнено или нет задание:
```commandline
@todo_app.post("/<int:todo_id>/toggle/", endpoint="toggle")
def toggle_todo(todo_id: int):
    todo: TodoItem = db.get_or_404(TodoItem, todo_id)
    todo.done = not todo.done
    db.session.commit()
    return redirect(url_for("todo_app.list"))
```
- Роут4 (post) удаляет запись в таблице и на веб странице:
```commandline
@todo_app.post("/<int:todo_id>/delete", endpoint="delete")
def delete_todo(todo_id: int):
    todo: TodoItem = db.get_or_404(TodoItem, todo_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("todo_app.list"))
```
Описание файла index.html (используем Jinja2):
В стандартный шаблон html (без CSS) добавляем python код, придающий странице динамические свойства.
1. Форма для добавления записи задания:
```commandline
  <div>
        <form method="post">
        <label for="todo-text-id">New todo:</label>
        <input
                id="todo-text-id"
                name="todo-text"
                type="text"
                required="required"
        >
            <button type="submit">ADD</button>
            {% with messages = get_flashed_messages() %}
            {% if messages %}
            <ul class="Flashes">
                {% for message in messages%}
                <li>{{ message }}</li>
                {% endfor %}
            </ul>
            {% endif%}
            {% endwith%}
        </form>
    </div>
```
Форма состоит из надписи (Lable), поля для ввода текста (блок input), кнопки.  
Еесли введено непустое значение, то в тег \<ul> (список) добавляется строка - тег \<li>  .

2. Следующая форма - форма списка с текстом задания и эмодзи, два из трех имеют свойства кнопки.
```commandline
<ul>
        {% for todo in todos %}
        <li style="margin-bottom: 3px">
            <form
                    style="display:inline;"
                    action="{{ url_for('todo_app.toggle', todo_id=todo.id) }}"
                    method="post"
            >
                <input type="submit" value="▶️️"/>
            </form>
            {{ todo.text }} {{ '✅' if todo.done else '⏺️' }}
            <form
                    style="display:inline;"
                    action="{{ url_for('todo_app.delete', todo_id=todo.id) }}"
                    method="post"
            >
                <input type="submit" value="❌"/>
            </form>
        </li>
        {% endfor %}
    </ul>
```
Процесс работы приложения представлен скринами нижe:

