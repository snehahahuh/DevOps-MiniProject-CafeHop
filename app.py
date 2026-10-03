from flask import Flask, render_template, request, redirect, url_for, session, Response
import json
import os

app = Flask(__name__)

app.secret_key = "cafehop-secret-key"

DATA_FILE = os.path.join("data", "cafes.json")

request_count = 0


@app.before_request
def count_requests():
    global request_count
    request_count += 1


def load_cafes():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


@app.route("/")
def home():

    cafes = load_cafes()

    search = request.args.get("search", "").strip().lower()
    category = request.args.get("category", "").strip().lower()
    min_rating = request.args.get("rating", "").strip()
    sort = request.args.get("sort", "").strip()

    if search:
        cafes = [
            cafe for cafe in cafes
            if search in cafe["name"].lower()
            or search in cafe["location"].lower()
            or search in cafe["category"].lower()
        ]

    if category:
        cafes = [
            cafe for cafe in cafes
            if category == cafe["category"].lower()
        ]

    if min_rating:
        try:
            rating = float(min_rating)

            cafes = [
                cafe for cafe in cafes
                if cafe["rating"] >= rating
            ]

        except ValueError:
            pass

    if sort == "high":
        cafes = sorted(
            cafes,
            key=lambda cafe: cafe["rating"],
            reverse=True
        )

    elif sort == "low":
        cafes = sorted(
            cafes,
            key=lambda cafe: cafe["rating"]
        )

    favorites = session.get("favorites", [])

    return render_template(
        "index.html",
        cafes=cafes,
        search=search,
        category=category,
        min_rating=min_rating,
        sort=sort,
        favorites=favorites
    )


@app.route("/cafe/<int:cafe_id>")
def cafe_details(cafe_id):

    cafes = load_cafes()

    cafe = next(
        (cafe for cafe in cafes if cafe["id"] == cafe_id),
        None
    )

    if cafe is None:
        return "Cafe not found", 404

    favorites = session.get("favorites", [])

    return render_template(
        "cafe.html",
        cafe=cafe,
        favorites=favorites
    )


@app.route("/favorite/<int:cafe_id>")
def toggle_favorite(cafe_id):

    cafes = load_cafes()

    cafe_exists = any(
        cafe["id"] == cafe_id
        for cafe in cafes
    )

    if not cafe_exists:
        return "Cafe not found", 404

    favorites = session.get("favorites", [])

    if cafe_id in favorites:
        favorites.remove(cafe_id)
    else:
        favorites.append(cafe_id)

    session["favorites"] = favorites

    return redirect(
        request.referrer or url_for("home")
    )


@app.route("/favorites")
def favorites():

    cafes = load_cafes()

    favorite_ids = session.get("favorites", [])

    favorite_cafes = [
        cafe for cafe in cafes
        if cafe["id"] in favorite_ids
    ]

    return render_template(
        "favorites.html",
        cafes=favorite_cafes
    )


@app.route("/metrics")
def metrics():

    metrics_data = f"""# HELP cafehop_requests_total Total number of requests received by CafeHop.
# TYPE cafehop_requests_total counter
cafehop_requests_total {request_count}

# HELP cafehop_up Indicates that the CafeHop application is running.
# TYPE cafehop_up gauge
cafehop_up 1
"""

    return Response(
        metrics_data,
        mimetype="text/plain"
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)