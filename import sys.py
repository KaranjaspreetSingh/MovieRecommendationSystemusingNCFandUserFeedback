import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit, QMessageBox
from PyQt5.QtGui import QPixmap
from io import BytesIO

# Replace this with your actual API key (for TMDb or IMDb alternative)
API_KEY = "4c533540f531d10140f964ccc97e9e9c"
API_URL = "https://api.themoviedb.org/3/movie/{movie_id}?api_key=" + "4c533540f531d10140f964ccc97e9e9c"

class MovieRecommendationApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Movie Recommendation System")
        self.setGeometry(100, 100, 400, 500)

        self.layout = QVBoxLayout()

        # User Login Fields
        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit(self)
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)

        # Login Button
        self.login_button = QPushButton("Login", self)
        self.login_button.clicked.connect(self.login)

        # Movie ID Input
        self.movie_id_label = QLabel("Enter Movie ID:")
        self.movie_id_input = QLineEdit(self)

        # Fetch Movie Button
        self.fetch_button = QPushButton("Fetch Movie", self)
        self.fetch_button.clicked.connect(self.fetch_movie)

        # Movie Name Display
        self.movie_name_label = QLabel("Movie Name: ")
        
        # Movie Poster Display
        self.movie_poster_label = QLabel()
        
        # Adding widgets to layout
        self.layout.addWidget(self.username_label)
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.login_button)
        self.layout.addWidget(self.movie_id_label)
        self.layout.addWidget(self.movie_id_input)
        self.layout.addWidget(self.fetch_button)
        self.layout.addWidget(self.movie_name_label)
        self.layout.addWidget(self.movie_poster_label)

        self.setLayout(self.layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if username == "admin" and password == "password":  # Replace with proper authentication
            QMessageBox.information(self, "Login Successful", "Welcome, " + username)
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password")

    def fetch_movie(self):
        movie_id = self.movie_id_input.text()

        if not movie_id:
            QMessageBox.warning(self, "Error", "Please enter a Movie ID")
            return

        try:
            response = requests.get(API_URL.format(movie_id=movie_id))
            data = response.json()

            if "title" in data:
                movie_name = data["title"]
                poster_path = data.get("poster_path", "")

                # Update movie name
                self.movie_name_label.setText(f"Movie Name: {movie_name}")

                if poster_path:
                    poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
                    poster_response = requests.get(poster_url)
                    pixmap = QPixmap()
                    pixmap.loadFromData(BytesIO(poster_response.content).read())
                    self.movie_poster_label.setPixmap(pixmap)
                    self.movie_poster_label.setScaledContents(True)
                else:
                    self.movie_poster_label.setText("Poster not available")

            else:
                QMessageBox.warning(self, "Error", "Invalid Movie ID or Movie not found!")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to fetch movie: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MovieRecommendationApp()
    window.show()
    sys.exit(app.exec_())
