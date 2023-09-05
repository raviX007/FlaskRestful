from app import db

class Movie(db.Model):
    __tablename__ = 'movie'
    mov_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    popularity99 = db.Column(db.Integer, nullable=True)
    director = db.Column(db.String(), nullable=True)
    genre = db.Column(db.JSON, nullable=True)  
    imdb_score = db.Column(db.Float, nullable=True)
    name = db.Column(db.String(), nullable=True)

    def __init__(self, popularity99, director, genre, imdb_score, name):
        self.popularity99 = popularity99
        self.director = director
        self.genre = genre
        self.imdb_score = imdb_score
        self.name = name

