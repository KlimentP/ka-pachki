from sqlalchemy import create_engine, text
import pandas as pd

user = "postgres"
password = "qCNb3EeEJhfarz7e"
host = "db.jqxnxdsmhkszzwchhicw.supabase.co"
port = "5432"
database = "postgres"
ssl_args = {'sslrootcert': 'prod-ca-2021.crt'}

# Create a connection string for SQLAlchemy
connection_string = f"postgresql://{user}:{password}@{host}:{port}/{database}"

cn_str2 = "postgresql://postgres:qCNb3EeEJhfarz7e@db.jqxnxdsmhkszzwchhicw.supabase.co:5432/postgres"
# Create a new SQLAlchemy engine
engine = create_engine(cn_str2, connect_args=ssl_args)
query = "select * from designs"

tt = pd.DataFrame(engine.connect().execute(text(query)))