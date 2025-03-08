import pickle
import sqlite3
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent

model_path = project_root / "assets/model.pkl"
db_path = project_root / "python-package/employee_events/employee_events.db"


def load_model():
    """Load and return the trained model from a pickle file."""
    with model_path.open("rb") as file:
        model = pickle.load(file)
    return model


def connect_db():
    """Establish and return a connection to the SQLite database."""
    return sqlite3.connect(db_path)
