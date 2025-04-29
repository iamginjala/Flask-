# Flask Cafe API

A simple Flask application providing a RESTful API to manage a list of cafes. Built with Flask and SQLAlchemy, it supports creating, reading, updating, and deleting cafes stored in a SQLite database.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
  - [Home Page](#home-page)
  - [Get Random Cafe](#get-random-cafe)
  - [Get All Cafes](#get-all-cafes)
  - [Search Cafes by Location](#search-cafes-by-location)
  - [Add a New Cafe](#add-a-new-cafe)
  - [Update Cafe Price](#update-cafe-price)
  - [Delete (Close) a Cafe](#delete-close-a-cafe)
- [Error Handling](#error-handling)
- [Contributing](#contributing)
- [License](#license)

## Features

- Store cafe details in a SQLite database
- Retrieve a random cafe or list all cafes
- Search cafes by location
- Add new cafes via POST requests
- Update cafe coffee prices via PATCH requests
- Delete (close) cafes via DELETE requests with API key authorization

## Prerequisites

- Python 3.7 or higher
- `pip` package manager

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/iamginjala/flask-
   cd your-repo-name
   ```
2. Install dependencies:
   ```bash
   # On Windows
   python -m pip install -r requirements.txt

   # On macOS/Linux
   pip3 install -r requirements.txt
   ```

## Configuration

- In the main application file, update the `SECRET_KEY` variable with your own secure key:
  ```python
  SECRET_KEY = 'your-secure-key-here'
  ```
- Optionally, you can extract this into an environment variable in a `.env` file and load it in your code.

## Database Setup

The app uses SQLite (`cafes.db`) by default. The database tables are created automatically when the app starts:

```python
with app.app_context():
    db.create_all()
```

If you need to reset the database, simply delete `cafes.db` and restart the app.

## Running the Application

Start the Flask development server with debug mode enabled:

```bash
python app.py
```

By default, it will run on `http://127.0.0.1:5000/`.

## API Endpoints

### Home Page

- **URL:** `/`
- **Method:** `GET`
- **Description:** Renders the homepage (`index.html`).

### Get Random Cafe

- **URL:** `/random`
- **Method:** `GET`
- **Description:** Returns a random cafe from the database.
- **Response:** JSON object with a single cafe.

```json
{
  "cafe": { ... }
}
```

### Get All Cafes

- **URL:** `/all`
- **Method:** `GET`
- **Description:** Returns a list of all cafes.
- **Response:** JSON array of cafe objects.

```json
[
  { ... },
  { ... }
]
```

### Search Cafes by Location

- **URL:** `/search?loc=<location>`
- **Method:** `GET`
- **Query Params:**
  - `loc` (required): The location to search for.
- **Description:** Returns all cafes matching the given location.
- **Responses:**
  - `200 OK` with JSON array of cafes if found.
  - `400 Bad Request` if `loc` is missing.
  - `404 Not Found` if no cafes match.

### Add a New Cafe

- **URL:** `/add`
- **Method:** `POST`
- **Form Data (application/x-www-form-urlencoded):**
  - `name`, `map_url`, `img_url`, `loc`, `sockets`, `toilet`, `wifi`, `calls`, `seats`, `coffee_price`
- **Description:** Adds a new cafe to the database.
- **Response:** JSON success message.

```json
{
  "response": {"success": "Successfully added the new cafe."}
}
```

### Update Cafe Price

- **URL:** `/update-price/<cafe_id>?new_price=<price>`
- **Method:** `PATCH`
- **Path Params:**
  - `cafe_id` (integer): The ID of the cafe to update.
- **Query Params:**
  - `new_price` (required): The new coffee price.
- **Description:** Updates the `coffee_price` field for the specified cafe.
- **Responses:**
  - `200 OK` on success.
  - `404 Not Found` if the cafe ID doesn’t exist.

### Delete (Close) a Cafe

- **URL:** `/report-closed/<cafe_id>?api_key=<key>`
- **Method:** `DELETE`
- **Path Params:**
  - `cafe_id` (integer): The ID of the cafe to delete.
- **Query Params:**
  - `api_key` (required): Your secret API key for authorization.
- **Description:** Deletes the specified cafe from the database.
- **Responses:**
  - `200 OK` on success.
  - `403 Forbidden` if the API key is invalid.
  - `404 Not Found` if the cafe ID doesn’t exist.

## Error Handling

The API returns appropriate HTTP status codes and JSON error messages for:

- Missing required parameters (`400 Bad Request`)
- Unauthorized access (`403 Forbidden`)
- Resource not found (`404 Not Found`)
- Database errors (`500 Internal Server Error`)

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on GitHub.

## License

This project is licensed under the MIT License. Feel free to use and modify it as needed.

