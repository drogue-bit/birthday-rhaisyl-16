import logging
from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

DEFAULT_STATS = {"views": "N/A", "followers": "N/A", "updates": "N/A"}
REQUEST_TIMEOUT = 10  # seconds


def get_stats(site_name):
    url = f"https://neocities.org/site/{site_name}"
    try:
        html = requests.get(url, timeout=REQUEST_TIMEOUT).text
        soup = BeautifulSoup(html, "html.parser")

        stats = {}
        stats_div = soup.find("div", class_="stats")
        if stats_div is None:
            logger.error("get_stats: could not find .stats div in neocities response")
            return DEFAULT_STATS.copy()

        for stat in stats_div.find_all("div", class_="stat"):
            label = stat.find("span").text.strip()
            value = stat.find("strong").text.strip()
            stats[label] = value

        return stats
    except requests.exceptions.Timeout:
        logger.error("get_stats: request to %s timed out after %ss", url, REQUEST_TIMEOUT)
        return DEFAULT_STATS.copy()
    except requests.exceptions.RequestException as e:
        logger.error("get_stats: request to %s failed: %s", url, e)
        return DEFAULT_STATS.copy()
    except Exception as e:
        logger.error("get_stats: unexpected error scraping %s: %s", url, e)
        return DEFAULT_STATS.copy()


def get_movies(site_name):
    url = "https://letterboxd.com/rhaisyl/films/"
    try:
        html = requests.get(url, timeout=REQUEST_TIMEOUT).text


        soup = BeautifulSoup(html, "html.parser")
        movies = []
        x = 0
        for img in soup.find_all("img"):
            alt = img.get("alt")
            x += 1
            if alt and alt not in movies and x != 1:
                movies.append(alt)

        return movies
    except requests.exceptions.Timeout:
        logger.error("get_movies: request to %s timed out after %ss", url, REQUEST_TIMEOUT)
        return []
    except requests.exceptions.RequestException as e:
        logger.error("get_movies: request to %s failed: %s", url, e)
        return []
    except Exception as e:
        logger.error("get_movies: unexpected error scraping %s: %s", url, e)
        return []


@app.route("/")
def home():
    try:
        stats = get_stats("rhaisyl")
    except Exception as e:
        print("Stats error:", e)
        stats = {}

    try:
        movies = get_movies("rhaisyl")
    except Exception as e:
        print("Movies error:", e)
        movies = []

    return render_template(
        "index.html",
        stats=stats,
        movies=movies,
        site_name="rhaisyl"
    )

if __name__ == "__main__":
    app.run(debug=True)
