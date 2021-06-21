from flask import Flask
from flask_restful import Api
from flask_cors import CORS 

from source import Problems

app = Flask(__name__)
api = Api(app)
CORS(app)

api.add_resource(Problems, '/')

if __name__ == '__main__':
    app.run()
