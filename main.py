import logging
from movie_app import MovieApp

def main():
    try:
        logging.basicConfig(level=logging.INFO)  # Logging
        movie_app = MovieApp()
        movie_app.run()
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
