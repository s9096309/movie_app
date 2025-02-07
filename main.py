from movie_app import MovieApp
from storage.storage_csv import StorageCsv

def main():
    # Create a StorageCsv object
    storage = StorageCsv('data/movies.csv')

    # Create a MovieApp object using the StorageCsv object
    movie_app = MovieApp(storage)

    # Run the MovieApp
    movie_app.run()  # Only add movie for now, as per new specification

if __name__ == "__main__":
    main()