from flask import Flask, render_template, request, redirect, url_for, flash
import folium
from folium.plugins import MarkerCluster
from flask_migrate import Migrate
from models import db, Place
import json


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///food_map.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "secret_key"
db.init_app(app)
migrate = Migrate(app, db)


# Memuat geojson agar bisa digunakan
with open("./static/json/semarang.geojson") as f:
    geojson_data = json.load(f)

# Preview map
preview_map = folium.Map(location=[-7.011374, 110.395078], zoom_start=12)

# Membuat polygon semarang
folium.GeoJson(
    geojson_data,
    style_function=lambda feature: {
        "color": "black",
        "weight": 2,
        "fillOpacity": 0.5,
    },
).add_to(preview_map)


@app.route("/")
def hello():

    return render_template("main/home.html", enable_scroll_nav=True)


@app.route("/map", methods=["GET", "POST"])
def map():
    if request.method == "POST":
        name = request.form["name"]
        lat = float(request.form["lat"])
        lon = float(request.form["lon"])
        img_url = request.form["img_url"]
        price_range = request.form["desc"]
        desc = request.form["desc"]

        new_place = Place(
            name=name,
            lat=lat,
            lon=lon,
            image_url=img_url,
            price_range=price_range,
            description=desc,
        )
        db.session.add(new_place)
        db.session.commit()
        flash("Berhasil Menambah data")
        return redirect(url_for("map"))

    return render_template("main/map.html", enable_scroll_nav=False)


if __name__ == "__main__":
    app.run(debug=True)
