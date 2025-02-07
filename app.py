from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    title = "My Movie App"
    movie_grid = [
        {"poster": "https://m.media-amazon.com/images/M/MV5BMThlMDA3NDYtZGM2Zi00NmJhLThlYWItZjViZTkzZWU1ZWRiXkEyXkFqcGc@._V1_SX300.jpg",
         "title": "La haine", "year": 1995, "rating": 8.1},
        {"poster": "https://m.media-amazon.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_SX300.jpg",
         "title": "Inception", "year": 2010, "rating": 8.8},
        {"poster": "https://m.media-amazon.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_SX300.jpg",
         "title": "Fight Club", "year": 1999, "rating": 8.8},
        {"poster": "https://m.media-amazon.com/images/M/MV5BNDUzYjY0NmUtMDM4OS00Y2Q5LWJiODYtNTk0ZTk0YjZhMTg1XkEyXkFqcGc@._V1_SX300.jpg",
         "title": "Scarface", "year": 1983, "rating": 8.3},
        {"poster": "https://m.media-amazon.com/images/M/MV5BN2FjNWExYzEtY2YzOC00YjNlLTllMTQtNmIwM2Q1YzBhOWM1XkEyXkFqcGc@._V1_SX300.jpg",
         "title": "Shutter Island", "year": 2010, "rating": 8.2}
    ]
    return render_template('index_template.html', title=title, movie_grid=movie_grid)

if __name__ == '__main__':
    app.run(debug=True)
