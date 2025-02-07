import requests

api_key = "1299a8a"
film_title = input("Gib den Filmtitel ein: ").strip()

url = f"http://www.omdbapi.com/?apikey={api_key}&t={film_title}"

response = requests.get(url)
print("Raw API Response:", response.text)  # DEBUG

if response.status_code == 200:
    data = response.json()
    if data.get('Response') == 'True':
        print(f"Title: {data['Title']}, Year: {data['Year']}")
    else:
        print("Movie not found. API Response:", data)  # DEBUG
else:
    print("Error during request:", response.status_code)
