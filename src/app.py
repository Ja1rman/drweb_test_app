from flask import Flask, request, send_file
from flask_restful import Resource, Api, reqparse
import werkzeug
import hashlib
import os

from database.db_manager import DatabaseManager
from services import config


app = Flask(__name__)
api = Api(app)
path_to_dir = os.path.abspath(os.getcwd())


class FileManager(Resource):
    method_decorators = {'post': [DatabaseManager.authenticate], 'delete': [DatabaseManager.authenticate]}

    def get(self):
        file_hash = request.args.getlist('hash')[0]
        filename = path_to_dir + f'/store/{file_hash[:2]}/{file_hash}'
        if not os.path.isfile(filename):
            return {'message': 'No file in storage'}, 404
        return send_file(filename)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('file', type=werkzeug.datastructures.FileStorage, required=True, location='files')
        file = parser.parse_args()['file']
        file_data = file.read()
        file_hash = hashlib.md5(file_data).hexdigest()
        filename = path_to_dir + f'/store/{file_hash[:2]}/{file_hash}'
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        status = DatabaseManager.add_hash_to_db(file_hash)
        if status[1] != 200:
            return status
        with open(filename, 'wb') as f:
            f.write(file_data)
        
        return {'hash': file_hash}, 201

    def delete(self):
        file_hash = request.args.getlist('hash')[0]
        filename = path_to_dir + f'/store/{file_hash[:2]}/{file_hash}'
        status = DatabaseManager.delete_hash_from_db(file_hash)
        if status[1] != 200:
            return status
        os.remove(filename)
        return {'message': 'The file was successfully deleted'}


api.add_resource(FileManager, '/api/file')
api.init_app(app)

if __name__ == '__main__':
    app.run(debug=True, host=config.APP_HOST, port=config.APP_PORT)
