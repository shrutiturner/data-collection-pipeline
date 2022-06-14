import boto3
import pandas as pd
from uuid import uuid4

import sqlalchemy

DATABASE_TYPE = 'postgresql'
DBAPI = 'psycopg2'
ENDPOINT = 'justgiving-scraper.czdhldofvzrb.eu-west-2.rds.amazonaws.com' # Change it for your AWS endpoint
USER = 'postgres'
PASSWORD = 'postgres'
PORT = 5432
DATABASE = 'postgres'

BUCKET_NAME = 'justgiving-scraper'

class AWS:

    def upload_file_method(self, file_name, object_name) -> str:
        """Function takes in an existing file and saves it to the names bucket in S3 with the specified name.

        Args:
            file_name (str): Name of file to be uploaded to S3.
            object_name (str): Desired name of file when saved in S3.

        Returns:
            str: URL of file in S3.
        """
        s3_client = boto3.client('s3')

        s3_client.upload_file(file_name, BUCKET_NAME, object_name)

        file_url = f's3://{BUCKET_NAME}/{object_name}'
        
        return file_url


    def write_to_rds(self, data) -> None:
        """Functions takes in a dictionary of data and saves this as a row to the specified database table.

        Args:
            data (dict): Dictionary of data to be saved to database.

        Returns:
            None: Code implents saving of data to cloud, but returns nothing.
        """
        rds_client = sqlalchemy.create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}")
        rds_client.connect()

        duplicates = rds_client.execute(f'SELECT * FROM fundraisers WHERE fundraisers.slug == {data["slug"]}').fetchall()

        if duplicates is None:
            data_df = pd.DataFrame(data, index=[str(uuid4())])
            data_df.to_sql('fundraisers', rds_client, if_exists='append')

        return None
