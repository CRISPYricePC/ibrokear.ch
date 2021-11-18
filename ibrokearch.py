import requests
import random
import os
from flask import Flask, redirect
from flask_caching import Cache

API_URL = "https://g.tenor.com/v1"
API_KEY = os.getenv("TENOR_API_KEY", "not_provided")

config = {
    "DEBUG": True,
    "CACHE_TYPE": "SimpleCache"
}
app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)


@cache.memoize(86400)
def get_tenor_gifs(search_term: str) -> list[str]:
    r = requests.get(
        f"{API_URL}/search?q={search_term}&key={API_KEY}&limit=50")
    results = r.json()["results"]
    return [result["media"][0]["mediumgif"]["url"] for result in results]


@app.route("/")
def skill_issue():
    gifs = get_tenor_gifs("skill issue")
    return redirect(random.choice(gifs))


if (__name__ == "__main__"):
    app.run(host="0.0.0.0")
