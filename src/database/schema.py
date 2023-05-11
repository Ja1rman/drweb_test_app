from database.db_engine import engine

from sqlalchemy import Table, Column, String, MetaData, ForeignKey

metadata = MetaData()
users_table = Table('users', metadata,
    Column('username', String, primary_key=True, nullable=False),
    Column('password', String, nullable=False),
)
hashes_table = Table('hashes', metadata,
    Column('hash', String, primary_key=True, nullable=False),
    Column('username', String, ForeignKey('users.username'), nullable=False),
    
)
metadata.create_all(engine)