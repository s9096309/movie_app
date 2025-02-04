from movie_app import MovieApp
from storage_json import StorageJson


def main():
    # Create a StorageJson object
    storage = StorageJson('movies.json')

    # Create a MovieApp object using the StorageJson object
    movie_app = MovieApp(storage)

    # Run the MovieApp
    movie_app.run()


if __name__ == "__main__":
    main()
