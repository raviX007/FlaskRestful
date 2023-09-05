from flask import request
from flask_login import  login_required
from flask_restful import Resource
from flask_cors import cross_origin
from app import db,login_manager

from flask_restful import request
from sqlalchemy import or_
from model import Movie




    
class MovieResource(Resource):
    
    @cross_origin(origin='*', supports_credentials=True)
    def post(self):
        try:
            role=request.headers.get('role')
            if role != 'admin':
                return {"message": "User role not authorized to insert record"}, 401
            data = request.get_json()
            
            if not isinstance(data, list):
                return {"message": "Invalid data format. Expected a list of movies."}, 400

            for movie_data in data:
                new_movie = Movie(
                    popularity99=movie_data['popularity99'],
                    director=movie_data['director'],
                    genre=movie_data['genre'],
                    imdb_score=movie_data['imdb_score'],
                    name=movie_data['name']
                )
                db.session.add(new_movie)

            db.session.commit()
            return {"message": "Movies created successfully"}, 201
        except Exception as e:
            db.session.rollback()
            return {"message": str(e)}, 500

    @cross_origin(origin='*', supports_credentials=True)
    def get(self, mov_id=None):
        try:
            name = request.args.get('name')
            min_imdb = request.args.get('min_imdb')
            director = request.args.get('director')
            genre = request.args.get('genre')
            year = request.args.get('year')
                        
            if mov_id is None:
                # Handle search based on query parameters

                # Start with a base query to select all movies
                base_query = Movie.query

                # Filter by IMDb score if 'min_imdb' is provided
                if min_imdb:
                    
                    base_query = base_query.filter(Movie.imdb_score >= min_imdb)

                # Filter by director if 'director' is provided
                if director:
                    
                    base_query = base_query.filter(Movie.director == director)

                # Filter by released year if 'year' is provided
                if year:
                    
                    base_query = base_query.filter(
                        or_(Movie.year_released == year, Movie.year_released.is_(None))
                    )

                # Filter by genre if 'genre' is provided
                if genre:
                    
                    base_query = base_query.filter(Movie.genre.contains([genre]))

                # Filter by name if 'name' is provided
                if name:
                    
                    base_query = base_query.filter(Movie.name == name)

                # Execute the final query and return results
                movies = base_query.all()

                # Serialize and return the movies
                movie_list = [
                    {
                        'mov_id': movie.mov_id,
                        'popularity99': movie.popularity99,
                        'director': movie.director,
                        'genre': movie.genre,
                        'imdb_score': movie.imdb_score,
                        'name': movie.name,
                    }
                    for movie in movies
                ]

                return movie_list
            else:
                # Handle retrieval of a single movie by mov_id
                movie = Movie.query.get(mov_id)
                if movie:
                    return {
                        'mov_id': movie.mov_id,
                        'popularity99': movie.popularity99,
                        'director': movie.director,
                        'genre': movie.genre,
                        'imdb_score': movie.imdb_score,
                        'name': movie.name,
                    }
                else:
                    return {"message": "Movie not found"}, 404
        except Exception as e:
            return {"message": str(e)}, 500

    @cross_origin(origin='*', supports_credentials=True)
    def put(self, mov_id):
        try:
            role=request.headers.get('role')
            if role != 'admin':
                return {"message": "User role not authorized to update record"}, 401
            movie = Movie.query.get(mov_id)
        
            if movie:
                data = request.get_json()
                movie.popularity99 = data['popularity99']
                movie.director = data['director']
                movie.genre = data['genre']
                movie.imdb_score = data['imdb_score']
                movie.name = data['name']
                db.session.commit()
                return {"message": "Movie updated successfully"}, 200
            else:
                return {"message": "Movie not found"}, 404
        except Exception as e:
            db.session.rollback()
            return {"message": str(e)}, 500
    
    @cross_origin(origin='*', supports_credentials=True)
    def delete(self, mov_id):
        try:
            role=request.headers.get('role')
            if role != 'admin':
                return {"message": "User role not authorized to delete record"}, 401
            movie = Movie.query.get(mov_id)
            if movie:
                db.session.delete(movie)
                db.session.commit()
                return {"message": "Movie deleted successfully"}, 200
            else:
                return {"message": "Movie not found"}, 404
        except Exception as e:
            db.session.rollback()
            return {"message": str(e)}, 500
   
   