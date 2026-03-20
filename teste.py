import json
from typing import Any

from pandas import read_sql
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.extensions.constants import CENSUS_TCP_HOST
from app.extensions.logger import new_logger

logger = new_logger()


def execute_query(query: str) -> dict[str, Any]:
    """Comando para execução de query
    Args:
      query: sql que será executado.
    """
    database = 'DWH_Gold_Daniel'
    user = 'daniel'
    password = '1234'
    logger.info("query received - %s", query)
    conn_string = (
        f"postgresql+psycopg2://{user}:{password}"
        f"@137.131.237.40:9000/{database}"
    )
    engine = create_engine(conn_string)
    session = sessionmaker(engine, expire_on_commit=False)
    with session() as conn:
        result = read_sql(text(query.replace("`", '"')), conn.bind).to_dict(
            "records"
        )
        return {"result": json.loads(json.dumps(result, default=str))}


def execute_query_total_daniel() -> dict[str, Any]:
    """executa query de valor"""
    return execute_query("select sum(vlr_total) from dwh_f_fato_vendas;")


def get_database_schema(database: str, user: str, password: str) -> str:
    query = """
    SELECT
        table_name, column_name, data_type
    FROM INFORMATION_SCHEMA.COLUMNS
    """
    schema = {}
    result = execute_query(database, user, password, query)["result"]
    for item in result:
        table = schema.setdefault(item["table_name"], {})
        table[item["column_name"]] = item["data_type"]
    create_statment = ""
    for table, columns in schema.items():
        if columns:
            columns_statment = ", ".join(
                f'"{column}" {type_}' for column, type_ in columns.items()
            )
            create_statment += f"CREATE TABLE {table} ({columns_statment});\n"
    return create_statment