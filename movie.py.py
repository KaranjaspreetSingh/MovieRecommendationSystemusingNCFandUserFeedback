import tkinter as tk
from tkinter import Label, Entry, Button, Scrollbar, Canvas
import requests
from PIL import Image, ImageTk
from io import BytesIO

# TMDB API Key (Replace with your own)
TMDB_API_KEY = "4c533540f531d10140f964ccc97e9e9c"

# Dummy data: Mapping user IDs to liked movie IDs (In practice, this would come from a database)
USER_LIKED_MOVIES = {
    "1": [550, 299536, 597],  # Example: Fight Club, Avengers: Infinity War, and Money Heist
    "2": [680, 155, 157336],  # Example: Pulp Fiction, The Dark Knight, and Interstellar
}

# Function to fetch movie recommendations from TMDB
def fetch_movie_recommendations(user_id):
    if user_id not in USER_LIKED_MOVIES:
        print("Invalid User ID")
        return []
    
    movie_ids = USER_LIKED_MOVIES[user_id]
    recommended_movies = []

    for movie_id in movie_ids:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}/recommendations?api_key={TMDB_API_KEY}&language=en-US"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            print(f"Recommendations for {movie_id}: {data['results']}")  # Debugging
            for movie in data.get("results", [])[:2]:  
                recommended_movies.append((movie["title"], f"https://image.tmdb.org/t/p/w500{movie['poster_path']}"))
        else:
            print(f"API Request Failed for {movie_id}: {response.status_code}, {response.text}")

    return recommended_movies[:6]

# Function to display movie recommendations
def display_movies():
    user_id = user_id_entry.get()
    canvas.delete("all")  # Clear previous results

    if not user_id:
        error_label.config(text="Enter a valid User ID")
        return
    
    movies = fetch_movie_recommendations(user_id)
    if not movies:
        error_label.config(text="No recommendations found")
        return

    error_label.config(text="")  # Clear error message

    x_offset, y_offset = 10, 10
    for title, poster_url in movies:
        try:
            response = requests.get(poster_url)
            img = Image.open(BytesIO(response.content))
            img = img.resize((120, 180), Image.Resampling.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)

            label = Label(canvas, image=img_tk, text=title, compound="top", wraplength=120)
            label.image = img_tk
            canvas.create_window(x_offset, y_offset, anchor="nw", window=label)

            x_offset += 140
            if x_offset > 400:  # Move to next row if width exceeds
                x_offset = 10
                y_offset += 200
        except:
            print(f"Failed to load image for {title}")

# Create GUI Window
root = tk.Tk()
root.title("Movie Recommendation System")
root.geometry("600x500")

# UI Elements
Label(root, text="Enter User ID:").pack(pady=5)
user_id_entry = Entry(root)
user_id_entry.pack(pady=5)

Button(root, text="Get Recommendations", command=display_movies).pack(pady=10)

error_label = Label(root, text="", fg="red")
error_label.pack()

# Scrollable Canvas for Movie Posters
canvas_frame = tk.Frame(root)
canvas_frame.pack(fill="both", expand=True)
canvas = Canvas(canvas_frame, width=550, height=350)
scroll_y = Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scroll_y.set)
canvas.pack(side="left", fill="both", expand=True)
scroll_y.pack(side="right", fill="y")

root.mainloop()
