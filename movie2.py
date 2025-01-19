import tkinter as tk
from tkinter import Label, Entry, Button, Scrollbar, Canvas, Frame
import requests
from PIL import Image, ImageTk
from io import BytesIO

# TMDB API Key (Replace with your own)
TMDB_API_KEY = "4c533540f531d10140f964ccc97e9e9c"

# Function to fetch movie ID from TMDB based on the title
def get_movie_id(movie_name):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_name}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        if data["results"]:
            return data["results"][0]["id"]  # Return the first matching movie ID
    except requests.exceptions.RequestException as e:
        print(f"Error fetching movie ID: {e}")
    return None

# Function to fetch movie recommendations dynamically
def fetch_movie_recommendations(movie_name):
    movie_id = get_movie_id(movie_name)
    if not movie_id:
        return []

    recommended_movies = []
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/recommendations?api_key={TMDB_API_KEY}&language=en-US"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        for movie in data.get("results", [])[:9]:  # Fetch top 9 recommendations
            if movie.get("poster_path"):
                recommended_movies.append((movie["title"], f"https://image.tmdb.org/t/p/w500{movie['poster_path']}"))
    except requests.exceptions.RequestException as e:
        print(f"API Request Failed: {e}")

    return recommended_movies

# Function to display movie recommendations
def display_movies():
    movie_name = movie_entry.get().strip()
    canvas.delete("all")  # Clear previous results

    if not movie_name:
        error_label.config(text="⚠ Enter a movie name")
        return

    movies = fetch_movie_recommendations(movie_name)
    if not movies:
        error_label.config(text="⚠ No recommendations found")
        return

    error_label.config(text="")  # Clear error message

    # Calculate grid positions
    canvas_width = root.winfo_width() - 50
    img_size = min(canvas_width // 5, 180)  # Resize images dynamically
    x_offset, y_offset = 20, 20
    col_count = max(1, canvas_width // (img_size + 20))  # Auto-adjust columns

    for idx, (title, poster_url) in enumerate(movies):
        try:
            response = requests.get(poster_url, timeout=5)
            response.raise_for_status()

            img = Image.open(BytesIO(response.content))
            img = img.resize((img_size, int(img_size * 1.5)), Image.Resampling.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)

            label = Label(canvas, image=img_tk, text=title, compound="top", wraplength=img_size, fg="white", bg="#222222", font=("Arial", max(10, img_size // 12), "bold"))
            label.image = img_tk  # Keep a reference
            canvas.create_window(x_offset, y_offset, anchor="nw", window=label)

            if (idx + 1) % col_count == 0:
                x_offset = 20
                y_offset += int(img_size * 1.8)  # Move to next row
            else:
                x_offset += img_size + 20  # Move to next column

        except requests.exceptions.RequestException as e:
            print(f"Failed to load image for {title}: {e}")

    canvas.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))  # Update scroll region

# Function to toggle fullscreen mode
def toggle_fullscreen(event=None):
    root.attributes("-fullscreen", not root.attributes("-fullscreen"))

# Create GUI Window
root = tk.Tk()
root.title("🎬 Movie Recommendation System")
root.geometry("1200x700")
root.state("zoomed")  # Start in maximized mode
root.configure(bg="#1c1c1c")

# Bind Fullscreen Toggle (Press F11)
root.bind("<F11>", toggle_fullscreen)
root.bind("<Escape>", lambda e: root.attributes("-fullscreen", False))

# Header Label
header_label = Label(root, text="Movie Recommendation System", font=("Helvetica", 18, "bold"), fg="white", bg="#1c1c1c")
header_label.pack(pady=10)

# Movie Name Input
frame_input = Frame(root, bg="#1c1c1c")
frame_input.pack(pady=10)
Label(frame_input, text="Enter a Movie Name:", font=("Arial", 14, "bold"), fg="white", bg="#1c1c1c").pack(side="left", padx=10)
movie_entry = Entry(frame_input, font=("Arial", 14), width=20, bg="#333333", fg="white", insertbackground="white")
movie_entry.pack(side="left", padx=10)

# Fetch Button
fetch_btn = Button(root, text="🎥 Get Recommendations", font=("Arial", 14, "bold"), bg="#ff5733", fg="white", relief="flat", command=display_movies)
fetch_btn.pack(pady=10)
fetch_btn.bind("<Enter>", lambda e: fetch_btn.config(bg="#ff784e"))  # Hover Effect
fetch_btn.bind("<Leave>", lambda e: fetch_btn.config(bg="#ff5733"))

# Error Label
error_label = Label(root, text="", fg="red", font=("Arial", 12, "bold"), bg="#1c1c1c")
error_label.pack()

# Scrollable Canvas for Movie Posters
canvas_frame = Frame(root, bg="#1c1c1c")
canvas_frame.pack(fill="both", expand=True, padx=10, pady=10)
canvas = Canvas(canvas_frame, bg="#222222", highlightthickness=0)
scroll_y = Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scroll_y.set)
canvas.pack(side="left", fill="both", expand=True)
scroll_y.pack(side="right", fill="y")

# Prevent unnecessary API calls when resizing
def resize_ui(event):
    canvas.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

root.bind("<Configure>", resize_ui)

# Run the GUI
root.mainloop()
