from pathlib import Path

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "todo-project.db"
SQLITE_DB_URI = f"sqlite:///{DB_PATH}"