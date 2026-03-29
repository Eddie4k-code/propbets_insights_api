import os
from db.postgres_db_connection import PostgresConnection
from dotenv import load_dotenv

load_dotenv()


# Shared DB connection for the whole app
db = PostgresConnection(connection_string=os.getenv("DATABASE_URL"))
db.initiate_connection()
