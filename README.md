**Movie Database Project**

**Purpose**

This project is a simple movie database application that stores movies either in a JSON or CSV file. A dynamic website is generated to display the movies with their posters, titles, and release years.

**Features**

- Storing and managing movies in a JSON (movies.json) or CSV file (movies.csv).
- Generation of a dynamic HTML page (index.html) using Flask.
- Selection between JSON or CSV data source via the configuration file (config.json).
- Responsive design for clear display.
- Automatic display of movie posters based on saved URLs.
- Flask backend for managing movie data (Add, Update, Delete).

**Setup**

1. Clone the repository:
```bash
git clone https://github.com/s9096309/movie_app.git
cd movie_app
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Adjust configuration:
The config.json file determines whether the data is loaded from a JSON or CSV file:

```json
{
    "storage_type": "json",  // Alternatively: "csv"
    "storage_file": "movies.json"
}
```
If CSV data is to be used, set `"storage_type": "csv"` and change `"storage_file"` accordingly.

5. Start the Flask application:
```bash
python main.py
```
The local development server runs at http://127.0.0.1:5000/.  
The generated website will display the movie data with posters and details.

**Data Format**

*JSON (movies.json)*:
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

*CSV (movies.csv)*:
```csv
title,rating,year,poster_url,imdbID
Inception,8.8,2010,https://image_url.com,tt1375666
```

**Web App Features**

- Add, update, and delete movies
- Load movies from JSON or CSV
- Dynamic HTML generation with Flask
- IMDb links for movies
- Optional rating visualization with Matplotlib

**Requirements**

This project requires Python 3.x and the following dependencies:

- Flask==3.1.0
- Requests==2.32.3
- Matplotlib~=3.9.2

**License**

This project is licensed under the MIT License.