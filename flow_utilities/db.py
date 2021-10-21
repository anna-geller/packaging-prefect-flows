import pandas as pd
from prefect.client import Secret
import sqlalchemy


def get_db_connection_string() -> str:
    user = Secret("DBT__POSTGRES_USER").get()
    pwd = Secret("DBT__POSTGRES_PASS").get()
    return f"postgresql://{user}:{pwd}@localhost:5432/postgres"


def get_df_from_sql_query(table_or_query: str) -> pd.DataFrame:
    db = get_db_connection_string()
    engine = sqlalchemy.create_engine(db)
    return pd.read_sql(table_or_query, engine)
