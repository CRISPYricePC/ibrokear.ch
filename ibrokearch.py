import requests
import random
import os
from io import BytesIO
from flask import Flask, send_file
from flask_caching import Cache

API_URL = "https://g.tenor.com/v1"
API_KEY = os.getenv("TENOR_API_KEY", "not_provided")

config = {
    "DEBUG": True,
    "CACHE_TYPE": "FileSystemCache",
    "CACHE_KEY_PREFIX": "SkillIssue",
    "CACHE_DEFAULT_TIMEOUT": 86400
}
for env_var in ["CACHE_DIR"]:
    config[env_var] = os.getenv(env_var)

app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)


@cache.memoize()
def get_tenor_gifs(search_term: str) -> list[str]:
    r = requests.get(
        f"{API_URL}/search?q={search_term}&key={API_KEY}&limit=50")
    results = r.json()["results"]
    return [result["media"][0]["gif"]["url"] for result in results]


@cache.memoize()
def pull_tenor_gif(url: str) -> BytesIO:
    r = requests.get(url)
    return BytesIO(r.content)


@app.route("/")
def skill_issue():
    file = pull_tenor_gif(random.choice(get_tenor_gifs("skill issue")))
    return send_file(file, mimetype="image/gif")


if (__name__ == "__main__"):
    app.run(host="0.0.0.0")
