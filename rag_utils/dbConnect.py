from dotenv import load_dotenv
from typing import Annotated
from sqlmodel import Field, Session, SQLModel, create_engine, select
import os
load_dotenv()

db_url = os.getenv("DATABASE_URL")
