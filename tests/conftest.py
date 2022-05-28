import pytest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from alembic.config import Config
from alembic import command
from tests.app_copy import create_app

database_url = os.environ.get("DATABASE_URL") if "postgresql" in os.environ.get("DATABASE_URL") else os.environ.get("DATABASE_URL").replace("postgres", "postgresql", 1)

def reset_db():
    e = create_engine(
        url=database_url
    )
    with Session(bind=e) as sess:
        sess.execute("DELETE FROM swap_user")
        sess.commit()
        sess.execute("DELETE FROM investment")
        sess.commit()


reset_db()


@pytest.fixture(scope="module")
def app():
    app = create_app()
    return app
