from sqlalchemy import create_engine, text
from models import metadata
from config import POSTGRES_URL  # Пример: "postgresql+psycopg2://user:password@localhost/dbname"
from logger_config import logger

def main():
    engine = create_engine(POSTGRES_URL)
    metadata.create_all(engine)
    logger.info("✅ Tables created successfully.")

if __name__ == "__main__":
    main()
