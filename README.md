
# Movie Database Project

## Purpose

This project is a simple movie database application that stores movies either in a JSON or CSV file. A dynamic website is generated to display the movies with their posters, titles, and release years.

## Features

- Storing and managing movies in a JSON (`movies.json`) or CSV (`movies.csv`) file.
- Generation of a dynamic HTML page (`index.html`) using Flask.
- Selection between JSON or CSV data source via user input.
- Responsive design for clear display.
- Automatic display of movie posters based on saved URLs.
- Flask backend for managing movie data (Add, Update, Delete).

## Setup

1. **Clone the repository:**

    ```bash
    git clone https://github.com/s9096309/movie_app.git
    cd movie_app
    ```

2. **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # For Windows: venv\Scripts\activate
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Configuration:**

    When you first run the application, you'll be prompted to choose the data source (either CSV or JSON). Your choice will be saved to the `config.json` file.

    Example of the `config.json` file:
    ```json
    {
        "DATA_SOURCE": "csv"  // Alternatively: "json"
    }
    ```

    - If you choose **CSV**, `"DATA_SOURCE": "csv"` will be saved in the config file.
    - If you choose **JSON**, `"DATA_SOURCE": "json"` will be saved instead.

5. **Start the Flask application:**

    ```bash
    python app.py
    ```

    The local development server runs at `http://127.0.0.1:5000/`.  
    The generated website will display the movie data with posters and details.

## Data Format

### JSON (movies.json):
```json
{
    "Inception": {
        "year": 2010,
        "rating": 8.8,
        "poster_url": "https://image_url.com",
        "imdbID": "tt1375666"
    }
}
```

### CSV (movies.csv):
```csv
title,rating,year,poster_url,imdbID
Inception,8.8,2010,https://image_url.com,tt1375666
```

## Web App Features

- Add, update, and delete movies.
- Load movies from JSON or CSV based on the user's input saved in `config.json`.
- Dynamic HTML generation with Flask.
- IMDb links for movies.
- Optional rating visualization with Matplotlib.

## Requirements

This project requires Python 3.x and the following dependencies:

- Flask==3.1.0
- Requests==2.32.3
- Matplotlib~=3.9.2
- python-dotenv==1.0.1

## License

This project is licensed under the MIT License.
