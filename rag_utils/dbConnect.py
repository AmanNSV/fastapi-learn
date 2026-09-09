from dotenv import load_dotenv
from typing import Annotated
from sqlmodel import Field, Session, SQLModel, create_engine, select
import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

load_dotenv()

db_url = os.getenv("DATABASE_URL")

if not db_url:
    raise RuntimeError(
        "DATABASE_URL is not set. Please add DATABASE_URL to your .env file."
    )

engine = create_engine(db_url, pool_pre_ping=True)

def db_connection():
    try:

        with engine.connect() as connection:

            result = connection.execute(
                text("SELECT version();")
            )

            version = result.scalar()

            result = connection.execute(
                text("""
                SELECT extname, extversion
                FROM pg_extension
                WHERE extname = 'vector';
                """)
            )

            vector_extension = result.fetchone()

            if vector_extension:
                print(
                    f"pgvector enabled: \n"
                    f"{vector_extension.extname} \n"
                    f"{vector_extension.extversion}"
                )
            else:
                print("WARNING: pgvector extension is not enabled.")


    except SQLAlchemyError as e:
            print("Database connection failed.")
            print(f"Error: {e}")

    finally:
        pass

# if __name__ == "__main__":
#     db_connection()