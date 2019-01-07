import pandas as pd
from sqlalchemy import create_engine
from anjuke.settings import DB_NAME


def get_engine():
    conn = 'sqlite:///../%s' % DB_NAME
    return create_engine(conn, echo=False)


# -----------

def calc_average_price(locate_a):
    df_o = pd.read_sql("""select 
                     locate_b,
                     count(*) as count,
                     sum(area) as total_area,
                     sum(price) as total_price
                    from anjuke_data 
                    where locate_a = '%s' 
                    group by locate_b """ % locate_a,
                       get_engine())

    count = df_o['count']
    total_area = df_o['total_area']
    total_price = df_o['total_price']

    df_o['average_price'] = total_price / total_area
    df_o['average_area'] = total_area / count

    df_o = df_o.sort_values(by='average_price')
    return df_o


# df = pd.read_sql("""select * from anjuke_data
#                     where locate_a = '%s' and locate_b = '%s' """ % ("浦东", "川沙"),
#                  get_engine())
#
# print(df['UNIT_PRICE'].std())
# print(df)

print(calc_average_price("长宁"))

# df = pd.read_sql("select sum(price) from anjuke_data")
# print(df)