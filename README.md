
---

## Movie Database Project

### Purpose
This project is a simple movie database application that stores movies in a JSON file and generates a dynamic website displaying the movies with their posters, titles, and release years.

### Features
- Store and manage movies in a JSON file (`movies.json`).
- Generate a dynamic HTML page (`index.html`) displaying the movie collection using Flask.
- Responsive design with CSS for a clean layout.
- Automatically fetch movie posters using stored URLs.
- A Flask-powered backend to manage movie data (add, update, and delete movies).

### Setup

#### 1. Clone the repository:
```bash
git clone https://github.com/s9096309/movie_app.git
cd movie_app
```

#### 2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

#### 3. Install dependencies:
```bash
pip install -r requirements.txt
```

#### 4. Run the Flask application:
```bash
python main.py
```

- This will start a local development server at `http://127.0.0.1:5000/`.
- You can view the movie database through your web browser by navigating to that address.

#### 5. View the generated website:
- The dynamic website (`index.html`) will be rendered by Flask when you visit the app in your browser.
- The website will automatically display the movie collection, including posters and details fetched from the `movies.json` file.

### Usage
- Movies are stored in `movies.json` in the format:
  ```json
  {
      "Inception": {
          "year": 2010,
          "rating": 8.8,
          "poster_url": "https://image_url.com"
      }
  }
  ```
- Use the Flask-powered app to manage movies, including adding new movies, updating ratings, or deleting entries.
- Run `main.py` to start the Flask server and interact with the movie database via the web interface.

### Requirements
This project requires Python 3.x and the following dependencies:
- Flask==3.1.0 (for serving the dynamic web app)
- Requests==2.32.3 (for fetching data, if needed)
- Matplotlib~=3.9.2 (for optional rating visualizations)

### License
This project is licensed under the MIT License.

---

This version makes it clear that Flask is used to power the dynamic web application and includes setup instructions for running the server. Let me know if you'd like to adjust or add anything else!