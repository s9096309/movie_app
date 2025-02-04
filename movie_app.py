import random
import matplotlib.pyplot as plt


class MovieApp:
    def __init__(self, storage):
        self._storage = storage

    def _command_list_movies(self):
        movies = self._storage.list_movies()
        if not movies:
            print("No movies found.")
        else:
            # Ensure that 'None' is handled correctly for the year
            sorted_movies = sorted(
                movies.items(),
                key=lambda x: (x[1].get('year') if x[1].get('year') is not None else float('inf')),
                reverse=True
            )

            print("Movies in Database:")
            for index, (title, movie) in enumerate(sorted_movies, start=1):
                year_display = movie['year'] if movie['year'] is not None else "Unknown"
                print(f"{index}. {title} ({year_display}) Rating: {movie['rating']:.1f}")

    def _command_add_movie(self):
        # Check if the movie already exists in the list
        existing_movies = self._storage.list_movies()
        movie_name = input("Enter the movie name to add: ").strip()

        if movie_name in existing_movies:
            print(f"ERROR: {movie_name} is already in the database.")
            return

        try:
            user_movie_rating = float(input("Enter your rating between 1 and 10: "))
            if 1 <= user_movie_rating <= 10:
                # Allow the user to skip the year by pressing Enter
                user_movie_year_input = input("Enter the movie release year (or press Enter if unknown): ").strip()

                if user_movie_year_input:  # If the user entered something, try converting to int
                    user_movie_year = int(user_movie_year_input)
                else:  # If the input is empty, set the year to None (unknown)
                    user_movie_year = None

                # Add the movie to storage
                self._storage.add_movie(movie_name, user_movie_year, user_movie_rating)

                # Display the movie information
                year_display = user_movie_year if user_movie_year is not None else "Unknown"
                print(
                    f"Added {movie_name} with rating {user_movie_rating}, released in {year_display}, to the database.")
            else:
                print("Invalid rating. Enter a number between 1 and 10.")
        except ValueError:
            print("Invalid rating. Please enter a numeric value.")

    def _command_delete_movie(self):
        movies = self._storage.list_movies()
        if not movies:
            print("No movies to delete.")
            return

        # Display the list of movies
        self._command_list_movies()

        try:
            # Ask for the index of the movie to delete (User input starts at 1)
            ask_user_index = int(input("Which movie do you want to delete? Enter a number: "))

            # Convert to zero-based index
            ask_user_index -= 1

            # Ensure that the index is valid
            if not (0 <= ask_user_index < len(movies)):
                print("Invalid input. Please enter a valid number.")
                return

            # Get the sorted list of movies
            sorted_movies = sorted(movies.items(),
                                   key=lambda x: (x[1].get('year') if x[1].get('year') is not None else float('inf')),
                                   reverse=True)

            # Get the title of the movie to be deleted
            movie_title = sorted_movies[ask_user_index][0]

            # Ask for confirmation from the user
            confirm = input(f"Are you sure you want to delete '{movie_title}'? (y/n): ").strip().lower()
            if confirm == 'y':
                self._storage.delete_movie(movie_title)
                print(f"'{movie_title}' has been deleted from the list.")
            else:
                print(f"'{movie_title}' was not deleted.")
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

    def _command_update_movie(self):
        movies = self._storage.list_movies()
        if not movies:
            print("No movies to update.")
            return

        # Display the list of movies
        self._command_list_movies()

        try:
            # Ask for the index of the movie to update (User input starts at 1)
            ask_user_index = int(input("Which movie do you want to update? Enter a number: "))

            # Convert to zero-based index
            ask_user_index -= 1

            # Ensure that the index is valid
            if not (0 <= ask_user_index < len(movies)):
                print("Invalid input. Please enter a valid number.")
                return

            # Get the sorted list of movies
            sorted_movies = sorted(movies.items(),
                                   key=lambda x: (x[1].get('year') if x[1].get('year') is not None else float('inf')),
                                   reverse=True)

            # Get the title of the movie to update
            movie_title = sorted_movies[ask_user_index][0]

            # Ask for a new rating
            new_rating = float(input(f"Enter the new rating for '{movie_title}' (1-10): "))
            if 1 <= new_rating <= 10:
                self._storage.update_movie(movie_title, new_rating)
                print(f"Updated '{movie_title}' with new rating: {new_rating}")
            else:
                print("Invalid rating. Please enter a number between 1 and 10.")
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

    def _command_movie_stats(self):
        movies = self._storage.list_movies()

        if not movies:
            print("No movies in the database to analyze.")
            return

        # Ensure we access the dictionary of movies
        ratings = [movie['rating'] for movie in
                   movies.values()]  # Use .values() to access the dictionaries
        avg_rating = sum(ratings) / len(ratings)
        sorted_ratings = sorted(ratings)

        median_rating = sorted_ratings[len(ratings) // 2] if len(ratings) % 2 == 1 else \
            (sorted_ratings[len(ratings) // 2 - 1] + sorted_ratings[len(ratings) // 2]) / 2

        max_rating = max(ratings)
        min_rating = min(ratings)

        # Find movies with maximum and minimum ratings
        best_movies = [title for title, movie in movies.items() if movie['rating'] == max_rating]
        worst_movies = [title for title, movie in movies.items() if movie['rating'] == min_rating]

        print("\nStatistics:")
        print(f"Average rating: {avg_rating:.2f}")
        print(f"Median rating: {median_rating:.2f}")
        print(f"Best movie(s): {', '.join(best_movies)} with a rating of {max_rating}")
        print(f"Worst movie(s): {', '.join(worst_movies)} with a rating of {min_rating}")

    def _command_search_movie(self):
        search_term = input("Enter the movie title or keyword to search: ").strip().lower()
        movies = self._storage.list_movies()
        found_movies = {title: info for title, info in movies.items() if search_term in title.lower()}
        if found_movies:
            for title, info in found_movies.items():
                print(f"{title} ({info['year']}) - Rating: {info['rating']}")
        else:
            print("No movies found with that title.")

    def _command_random_movie(self):
        movies = self._storage.list_movies()
        if not movies:
            print("No movies available.")
            return
        movie = random.choice(list(movies.items()))
        print(f"Random Movie: {movie[0]} ({movie[1]['year']}) - Rating: {movie[1]['rating']}")

    def _command_sort_movies(self):
        movies = self._storage.list_movies()
        if not movies:
            print("No movies to sort.")
            return

        # Ask the user for the sorting order
        sort_order = input("Do you want to sort movies in ascending or descending order? (a/d): ").strip().lower()

        # Ensure the input is either 'a' or 'd'
        while sort_order not in ['a', 'd']:
            sort_order = input("Invalid input. Please enter 'a' for ascending or 'd' for descending: ").strip().lower()

        # Sort movies by rating
        sorted_movies = sorted(movies.items(), key=lambda x: x[1]['rating'], reverse=(sort_order == 'd'))

        # Output the sorted movies
        for title, info in sorted_movies:
            print(f"{title} ({info['year']}) - Rating: {info['rating']}")

    def _command_show_as_histogram(self):
        movies = self._storage.list_movies()
        if not movies:
            print("No movies to display.")
            return

        # Ensure we are accessing the 'rating' of the movies
        ratings = []
        for title, movie in movies.items():
            print(f"Checking movie: {title}, Rating: {movie.get('rating')}")  # Debug output
            if isinstance(movie, dict) and 'rating' in movie and movie['rating'] is not None:
                ratings.append(movie['rating'])

        if ratings:
            plt.hist(ratings, bins=10, edgecolor='black')
            plt.title('Movie Ratings Histogram')
            plt.xlabel('Rating')
            plt.ylabel('Frequency')
            plt.show()
        else:
            print("No valid ratings found to display.")

    def run(self):
        while True:
            print("""*** Welcome to My Movies Database ***
    1. List movies
    2. Add movie
    3. Delete movie
    4. Update movie
    5. Stats
    6. Random movie
    7. Search movie
    8. Sort Movies
    9. Show as histogram
    0. Exit
            """)
            user_input = input("Enter choice (0-9): ")
            while not user_input.isdigit() or not (0 <= int(user_input) <= 9):
                user_input = input("Invalid choice. Please enter a number between 0 and 9: ")
            user_input = int(user_input)

            if user_input == 1:
                self._command_list_movies()
            elif user_input == 2:
                self._command_add_movie()
            elif user_input == 3:
                self._command_delete_movie()
            elif user_input == 4:
                self._command_update_movie()
            elif user_input == 5:
                self._command_movie_stats()
            elif user_input == 6:
                self._command_random_movie()
            elif user_input == 7:
                self._command_search_movie()
            elif user_input == 8:
                self._command_sort_movies()
            elif user_input == 9:
                self._command_show_as_histogram()
            elif user_input == 0:
                print("Exiting the program... Bye!")
                break
