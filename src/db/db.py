from sqlalchemy import create_engine

DB = "postgres"  # ideally an env var
DB_HOST = "db"  # ideally an env var
DB_PORT = 5432  # ideally an env var
DB_USER = "postgres"  # ideally an env var
DB_PASS = "postgres"  # ideally an env var


def get_engine(db=DB, host=DB_HOST, port=DB_PORT, user=DB_USER, pwd=DB_PASS):
    db_url = f'postgresql://{user}:{pwd}@{host}:{port}/{db}'
    engine = create_engine(db_url, pool_size=40)
    return engine