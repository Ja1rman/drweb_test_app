from sqlalchemy import create_engine
from services import config

db_url = f'postgresql://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}'
engine = create_engine(db_url)
