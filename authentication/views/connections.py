import pymysql
import sqlalchemy
import pandas as pd


def data_fetcher_vindiata(sql_query, *args):
    conn = pymysql.connect(
        host='vindiata-mumbai-test-rds.czf66biuqkjr.ap-south-1.rds.amazonaws.com',
        user='root',
        password='6F3ZvpC2vTDgKA2L',
        db='vincontest',
        port=3306,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)

    cursor = conn.cursor()

    cursor.execute(sql_query, args)
    data = cursor.fetchall()

    df = pd.DataFrame(data)

    if len(df) == 0:
        df = pd.DataFrame({'Date': [args[1]], 'Value': [0]})
    cursor.close()
    conn.close()

    return df


def write_data(sql_query, *args):
    conn = pymysql.connect(
        host='vindiata-mumbai-test-rds.czf66biuqkjr.ap-south-1.rds.amazonaws.com',
        user='root',
        password='6F3ZvpC2vTDgKA2L',
        db='sfl_faboom',
        port=3306,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)

    cur = conn.cursor()
    cur.execute(sql_query, args)

    result = conn.commit()

    cur.close()
    conn.close()

    return result
