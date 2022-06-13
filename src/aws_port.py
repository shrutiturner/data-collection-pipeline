import boto3
import pandas as pd
from uuid import uuid4

from sqlalchemy import create_engine



DATABASE_TYPE = 'postgresql'
DBAPI = 'psycopg2'
ENDPOINT = 'justgiving-scraper.czdhldofvzrb.eu-west-2.rds.amazonaws.com' # Change it for your AWS endpoint
USER = 'postgres'
PASSWORD = 'postgres'
PORT = 5432
DATABASE = 'postgres'

BUCKET_NAME = 'justgiving-scraper'

class AWS:
    def __init__(self) -> None:
        self.s3_client = boto3.client('s3')
        
        self.rds_client = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}")
        self.rds_client.connect()
        

    def upload_file(self, file_name, object_name) -> str:
        self.s3_client.upload_file(file_name, BUCKET_NAME, object_name)

        file_url = f's3://{BUCKET_NAME}/{object_name}'

        return file_url


    def write_to_rds(self, data) -> None:

        data_df = pd.DataFrame(data, index=[str(uuid4())])
        data_df.to_sql('fundraisers', self.rds_client, if_exists='append')

        return None
