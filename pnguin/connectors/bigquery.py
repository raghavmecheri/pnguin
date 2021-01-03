def bigquery_conn():
    """Connect to a BigQuery instance using the variables in your environment

    Rather than exporting variables, rely on the bash environment.
    Running `export GOOGLE_APPLICATION_CREDENTIALS=my_creds.json` may be required

    Returns:
            google.cloud.bigquery.client.Client: A BigQuery client object

    """
    from google.cloud import bigquery

    return bigquery.Client()
