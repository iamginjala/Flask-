from flask import Flask, render_template, request, redirect, url_for, jsonify
import hashlib
import redis_client  # Module to interact with Redis

app = Flask(__name__)

BASE_URL = "http://localhost:5000/"  # Change this to your actual domain if deployed

def generate_short_url(long_url):
    return hashlib.md5(long_url.encode()).hexdigest()[:6]

@app.route("/")
def home():
    short_url = request.args.get("short_url")  # Get short_url if redirected
    full_short_url = f"{BASE_URL}{short_url}" if short_url else None
    return render_template("index.html", short_url=full_short_url)

@app.route("/shorten/<path:long_url>")
def shorten(long_url):
    short_url = generate_short_url(long_url)
    redis_client.save_url(short_url, long_url)

    # Redirect to home page and pass the full short URL
    return redirect(url_for("home", short_url=short_url))

@app.route('/<short_url>')
def redirect_to_url(short_url):
    long_url = redis_client.get_url(short_url)
    if long_url:
        return redirect(long_url, code=302)  # Redirect to original URL
    return jsonify({'error': 'URL not found'}), 404

if __name__ == "__main__":
    app.run(debug=True)
