def mysql_conn(
    host: str = "localhost",
    port: int = 3306,
    user: str = "root",
    db_name: str = "newbook",
):
    import pymysql.cursors

    return pymysql.connect(
        host=host,
        port=port,
        db=db_name,
        user=user,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )


def bigquery_conn():
    from google.cloud import bigquery

    return bigquery.Client()
