from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_stats(site_name):
    url = f"https://neocities.org/site/{site_name}"

    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    stats = {}

    for stat in soup.find("div", class_="stats").find_all("div", class_="stat"):
        label = stat.find("span").text.strip()
        value = stat.find("strong").text.strip()
        stats[label] = value

    return stats

def get_movies(site_name):
    html = requests.get("https://letterboxd.com/rhaisyl/films/").text

    with open("letterboxd.html", "w", encoding="utf-8") as f:
        f.write(html)

    soup = BeautifulSoup(html, "html.parser")
    movies = []
    x = 0
    for img in soup.find_all("img"):
        alt = img.get("alt")
        x += 1
        if alt and alt not in movies and x != 1:
            movies.append(alt)

    return movies

@app.route("/")
def home():
    stats = get_stats("rhaisyl")
    movies = get_movies("rhaisyl")

    return render_template(
        "index.html",
        stats=stats,
        movies=movies,
        site_name="rhaisyl"
    )
app.run(debug=True)