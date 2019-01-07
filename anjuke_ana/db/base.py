from sqlalchemy import create_engine
from anjuke.settings import DB_NAME
import pandas as pd


def get_engine():
    conn = 'sqlite:///../%s' % DB_NAME
    return create_engine(conn, echo=False)


def read_sql(sql, log=False):
    if log:
        print("sql > {sql}".format(sql=sql))
    return pd.read_sql(sql, get_engine())
