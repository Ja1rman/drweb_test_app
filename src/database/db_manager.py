from flask import request
from functools import wraps
from sqlalchemy import insert
import traceback
import hashlib

from database.db_engine import engine
from database.schema import users_table, hashes_table


class DatabaseManager:
    conn = engine.connect()
    
    @classmethod
    def authenticate(cls, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if request.authorization is None:
                return {'message': 'Login required!'}, 401
            username = request.authorization.username
            password = hashlib.md5(str.encode(request.authorization.password)).hexdigest()
            user_in_db = cls.conn.execute(users_table.select().where(users_table.c.username==username)).fetchall()
            cls.conn.commit()
            if len(user_in_db) != 0 and password == user_in_db[0][1]:
                return func(*args, **kwargs)
            else:
                return {'message': 'Login required!'}, 401
            
        return wrapper
    
    @classmethod
    def add_hash_to_db(cls, file_hash):
        username = request.authorization.username
        trans = cls.conn.begin()
        try:
            cls.conn.execute(insert(hashes_table).values(hash=file_hash, username=username))
            
        except:
            print(traceback.format_exc())
            trans.rollback()
            hash_in_db = cls.conn.execute(hashes_table.select().where(hashes_table.c.hash==file_hash)).fetchall()
            if len(hash_in_db) > 0:
                return {'message': 'File already exists.'}, 400
            else:
                return {'message': 'Server can\'t add file.'}, 500
        trans.commit()
        return {'message': 'OK'}, 200
    
    @classmethod
    def delete_hash_from_db(cls, file_hash):
        username = request.authorization.username
        trans = cls.conn.begin()
        try:
            deleted_files = cls.conn.execute(hashes_table.delete().where((hashes_table.c.hash==file_hash) & (hashes_table.c.username==username)).returning(hashes_table.c.hash, hashes_table.c.username)).fetchall()
        except:
            print(traceback.format_exc())
            trans.rollback()
            return {'message': 'Server can\'t delete file.'}, 500
        trans.commit()
        if len(deleted_files) == 0:
            return {'message': 'Your file was not found'}, 404
        return {'message': 'OK'}, 200
