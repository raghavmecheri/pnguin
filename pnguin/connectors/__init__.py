"""A collection of connectors/connection helpers to be used with pnguin
"""


def bigquery_conn():
    """Connect to a BigQuery instance using the variables in your environment

    Rather than exporting variables, rely on the bash environment.
    Running `export GOOGLE_APPLICATION_CREDENTIALS=my_creds.json` may be required

    Returns:
            google.cloud.bigquery.client.Client: A BigQuery client object

    """
    from google.cloud import bigquery

    return bigquery.Client()


def mysql_conn(
    host: str = "localhost",
    port: int = 3306,
    user: str = "root",
    db_name: str = "newbook",
):
    """Establish a PyMySQL connection object

    Connect to a MySQL Database to be used with a pnguin RemoteFrame

    Args:
        host (str): A hostname
        port (int): A port number
        user (str): A DB user
        db_name (str): The DB name being connected to

    Returns:
        pymysql.connections.Connection: Representation of a socket to a MySQL server

    """
    import pymysql.cursors

    return pymysql.connect(
        host=host,
        port=port,
        db=db_name,
        user=user,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )
