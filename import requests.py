import requests

TMDB_API_KEY = "4c533540f531d10140f964ccc97e9e9c"
MOVIE_ID = 550  # Example: Fight Club

url = f"https://api.themoviedb.org/3/movie/{MOVIE_ID}/recommendations?api_key={TMDB_API_KEY}&language=en-US"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print(data["results"])  # Check if recommendations exist
else:
    print("API Error:", response.status_code, response.text)
