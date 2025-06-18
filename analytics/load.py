import pandas as pd
from psycopg2.extras import execute_values


def bulk_upsert(df, table_name, conn, conflict_cols=None, update_cols=None):
    conflict_cols = conflict_cols or []
    update_cols = update_cols or []

    cols = list(df.columns)
    values = df.values.tolist()

    base_sql = f"INSERT INTO {table_name} ({', '.join(cols)}) VALUES %s"

    if conflict_cols:
        conflict_str = ", ".join(conflict_cols)
        update_str = ", ".join([f"{col} = EXCLUDED.{col}" for col in update_cols])
        sql = f"""
        {base_sql}
        ON CONFLICT ({conflict_str}) DO UPDATE SET
        {update_str}
        """
    else:
        sql = base_sql

    with conn.cursor() as cur:
        execute_values(cur, sql, values)
        conn.commit()


def bulk_delete(conn, table_name, key_columns, df):
    if df.empty:
        return

    key_tuples = list(df[key_columns].itertuples(index=False, name=None))
    if not key_tuples:
        return

    cols = ', '.join(key_columns)
    temp_table = ', '.join([f"{col}" for col in key_columns])
    sql = f"""
        DELETE FROM {table_name}
        USING (VALUES %s) AS vals ({cols})
        WHERE {table_name}.{key_columns[0]} = vals.{key_columns[0]} AND
              {table_name}.{key_columns[1]} = vals.{key_columns[1]}
    """

    with conn.cursor() as cur:
        execute_values(cur, sql, key_tuples)
        conn.commit()

