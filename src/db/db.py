from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import Session

DB = "postgres"  # ideally an env var
DB_HOST = "db"  # ideally an env var
DB_PORT = 5432  # ideally an env var
DB_USER = "postgres"  # nosec # ideally an env var
DB_PASS = "postgres"  # nosec # ideally an env var


def get_engine(db=DB, host=DB_HOST, port=DB_PORT, user=DB_USER, pwd=DB_PASS):
    db_url = f"postgresql://{user}:{pwd}@{host}:{port}/{db}"
    engine = create_engine(db_url, pool_size=40)
    return engine


class DB:
    def __init__(self, engine=None):
        if not engine:
            self.engine = get_engine()

    def write_entities(self, entities) -> None:
        with Session(self.engine) as session:
            session.add_all(entities)
            session.commit()

    def get_event_dates(self, entity: object, columns: list = None) -> list[object]:
        if columns:
            if len(columns) == 1:
                raise NotImplementedError()
            else:
                raise NotImplementedError()
        else:
            event_select_stmt = select(entity.e_date)
            with Session(bind=self.engine, expire_on_commit=False) as session:
                result = session.execute(event_select_stmt).scalars().all()

        return result
