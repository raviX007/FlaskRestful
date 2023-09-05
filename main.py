from flask import Flask
from flask_restful import Api
from resources import MovieResource
from app import app


api = Api(app)
api.add_resource(MovieResource, '/movie', '/movie/<int:mov_id>')

if __name__ == '__main__':
    app.run(debug=True)
