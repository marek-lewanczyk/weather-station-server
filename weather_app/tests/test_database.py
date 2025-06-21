from sqlalchemy.orm import Session
from weather_app import database

def test_sessionlocal_creates_valid_session():
    session = database.SessionLocal()
    assert isinstance(session, Session)
    session.close()

def test_get_db_yields_session():
    gen = database.get_db()
    session = next(gen)
    assert isinstance(session, Session)
    try:
        next(gen)
    except StopIteration:
        pass