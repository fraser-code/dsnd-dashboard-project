import pytest
from pathlib import Path
from sqlite3 import connect

import pandas as pd

from employee_events.employee import Employee
from employee_events.team import Team

project_root = Path(__file__).resolve().parent.parent


@pytest.fixture
def db_path():
    return project_root / "python_package" / "employee_events" / "employee_events.db"


def test_db_exists(db_path):
    assert db_path.is_file()


@pytest.fixture
def db_conn(db_path):
    return connect(db_path)


@pytest.fixture
def table_names(db_conn):
    name_tuples = db_conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table';"
    ).fetchall()
    return [x[0] for x in name_tuples]


def test_employee_table_exists(table_names):
    assert "employee" in table_names


def test_team_table_exists(table_names):
    assert "team" in table_names


def test_employee_events_table_exists(table_names):
    assert "employee_events" in table_names


@pytest.fixture
def employee_instance():
    return Employee()


@pytest.fixture
def team_instance():
    return Team()


def test_employee_names(employee_instance):
    names = employee_instance.names()
    assert isinstance(names, pd.DataFrame)
    assert not names.empty
    assert "full_name" in names.columns
    assert "employee_id" in names.columns


def test_employee_username(employee_instance):
    username = employee_instance.username(1)
    assert isinstance(username, pd.DataFrame)
    assert not username.empty
    assert "full_name" in username.columns


def test_employee_model_data(employee_instance):
    model_data = employee_instance.model_data(1)
    assert isinstance(model_data, pd.DataFrame)
    assert not model_data.empty
    assert "positive_events" in model_data.columns
    assert "negative_events" in model_data.columns


def test_team_names(team_instance):
    names = team_instance.names()
    assert isinstance(names, pd.DataFrame)
    assert not names.empty
    assert "team_name" in names.columns
    assert "team_id" in names.columns


def test_team_username(team_instance):
    username = team_instance.username(1)
    assert isinstance(username, pd.DataFrame)
    assert not username.empty
    assert "team_name" in username.columns


def test_team_model_data(team_instance):
    model_data = team_instance.model_data(1)
    assert isinstance(model_data, pd.DataFrame)
    assert not model_data.empty
    assert "positive_events" in model_data.columns
    assert "negative_events" in model_data.columns


def test_event_counts(employee_instance):
    event_counts = employee_instance.event_counts(1)
    assert isinstance(event_counts, pd.DataFrame)
    assert not event_counts.empty
    assert "event_date" in event_counts.columns
    assert "positive_events" in event_counts.columns
    assert "negative_events" in event_counts.columns


def test_notes(employee_instance):
    notes = employee_instance.notes(1)
    assert isinstance(notes, pd.DataFrame)
    assert not notes.empty
    assert "note_date" in notes.columns
    assert "note" in notes.columns
