import json
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, "config", "config.json")  # Pfad zur Konfigurationsdatei

def save_data_source(source):
    """Saves the selected data source in config.json."""
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)  # Creates the directory if it doesn't exist
    with open(CONFIG_FILE, "w") as f:
        json.dump({"DATA_SOURCE": source}, f, indent=4)

def load_data_source():
    """Loads the saved data source from config.json."""
    try:
        with open(CONFIG_FILE, "r") as f:
            content = f.read().strip()
            if not content:
                raise ValueError("File is empty")
            config = json.loads(content)
            return config.get("DATA_SOURCE", "csv")  # Default to "csv" if not set
    except (FileNotFoundError, json.JSONDecodeError, ValueError):
        # If the file doesn't exist or is invalid, assume CSV
        return "csv"
