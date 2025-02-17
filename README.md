## Movie Database Project

### Purpose
This project is a simple movie database application that stores movies in a JSON file and generates a static website displaying the movies with their posters, titles, and release years.

### Features
- Store and manage movies in a JSON file (`movies.json`).
- Generate a static HTML page (`index.html`) displaying the movie collection.
- Responsive design with CSS for a clean layout.
- Automatically fetch movie posters using stored URLs.

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

#### 4. Run the application:
```bash
python main.py
```

#### 5. View the generated website:
- The static website (`index.html`) will be available in the `static/` folder after running the script.
- Open `static/index.html` in a web browser to view the movie collection.

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
- Run `main.py` to regenerate the static website with updated movie data.

### Requirements
This project requires Python 3.x and the following dependencies:
- Flask==3.1.0 (for rendering templates)
- Requests==2.32.3 (for fetching data, if needed)
- Matplotlib~=3.9.2 (for optional rating visualizations)

### License
This project is licensed under the MIT License.

