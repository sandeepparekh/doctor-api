import os
from sqlalchemy import create_engine, MetaData
from databases import Database
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy engine and metadata
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Async database connection
database = Database(DATABASE_URL)
