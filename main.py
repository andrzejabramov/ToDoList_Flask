from dataclasses import dataclass
from flask import Flask
from flask_migrate import Migrate
import config
from models import db
from views.todo_items import todo_app


app = Flask(__name__)
app.config.update(
    SECRET_KEY="ytfhgjhjhjhjh465765",
    SQLALCHEMY_DATABASE_URI=config.SQLITE_DB_URI,
)
db.init_app(app)
migrate = Migrate(app, db=db)

app.register_blueprint(todo_app)


if __name__ == '__main__':
    app.run(debug=True)