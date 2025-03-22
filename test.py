'''import flet as ft

import requests

# Replace with your TMDB API key
api_key = "44e219fffa2a2b5852895fd8fe5bc463"

# Replace with the movie name
movie_name = "Inception"

# Make a GET request to the TMDB API's search endpoint
response = requests.get(f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_name}")

# Parse the JSON response
data = response.json()

# Get the first search result's ID
movie_id = data["results"][0]["id"]

# Make a GET request to the TMDB API to retrieve the movie's details
response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}")

# Parse the JSON response
data = response.json()

# Get the poster path
poster_path = data["poster_path"]

# Construct the full URL of the movie poster image
image_url = f"https://image.tmdb.org/t/p/w500/{poster_path}"

print(image_url)
def main(page:ft.Page):
    page.add(ft.Image(src=image_url))
ft.app(main)'''

a = 'data'
del(a)
print(a)