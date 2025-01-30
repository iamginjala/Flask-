# Flask Blog Application

This is a simple Flask-based blog application that fetches blog posts from an external API and displays them on a web page. Users can view all blog posts on the homepage and click on individual posts to see their full content.

## Features
- Fetches blog posts from an external API.
- Displays all blog posts on the homepage.
- Allows users to view full content of a selected blog post.
- Uses Flask for backend routing.
- Uses HTML and CSS for frontend design.
## How the Project Works
The application follows the Model-View-Controller (MVC) pattern:
Model (post.py): Defines the Post class structure.
View (templates/): HTML files render the blog data to the user.
Controller (main.py): Manages application logic and routing.

## Tech Stack
- **Backend:** Flask (Python)
- **Frontend:** HTML, CSS
- **Data Source:** JSON API (`https://api.npoint.io/c790b4d5cab58020d391`)

## Installation
### Prerequisites
Ensure you have Python installed (version 3.x recommended). You can check your Python version by running:
```sh
python --version
```

2. **Create a Virtual Environment (Optional but Recommended):**
```sh
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows
```

3. **Install Dependencies:**
```sh
pip install flask requests
```

4. **Run the Application:**
```sh
python main.py
```

5. **Access the Application:**
Open your browser and go to:
```
http://127.0.0.1:5000/
```

## Project Structure
```
flask-blog/
│── static/
│   └── css/
│       └── styles.css  # CSS styles
│── templates/
│   ├── index.html  # Homepage displaying all blog posts
│   ├── post.html  # Individual blog post page
│── main.py  # Main Flask application
│── post.py  # Post model
│── README.md  # Documentation
```

## API Data Source
The blog posts are fetched from the following API:
```
https://api.npoint.io/c790b4d5cab58020d391
```
Each post contains:
- `id`: Unique identifier
- `title`: Post title
- `subtitle`: Short description
- `body`: Full content
