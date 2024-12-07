from flask import Flask, render_template, request, redirect, url_for, flash
import folium
from folium.plugins import MarkerCluster
from flask_migrate import Migrate
from models import db, Place
import json
import googlemaps


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///food_map.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["GOOGLE_API_KEY"] = (
    "AIzaSyCU4mFWGN9UjhKUXYoEfcQR-TLmHfPPN98"  # MASUKKAN API KEY MILIK KAMU
)
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

preview_map.save("static/preview/preview_map.html")


@app.route("/")
def home():
    return render_template("main/home.html", enable_scroll_nav=True)


@app.route("/map", methods=["GET", "POST"])
def map():
    if request.method == "POST":
        name = request.form["name"]
        lat = float(request.form["lat"])
        lon = float(request.form["lon"])
        img_url = request.form["img_url"]
        price_range = request.form["price_range"]
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

    marker_cluster = MarkerCluster().add_to(preview_map)
    places = Place.query.all()
    for place in places:
        popup_content = f"""
        <b>{place.name}</b><br>
        {place.description}<br>
        <img src='{place.image_url}' width='200'><br>
        Rating: ⭐⭐⭐⭐⭐ 5/5<br>
        Harga: {place.price_range}
        """
        folium.Marker([place.lat, place.lon], popup=popup_content).add_to(
            marker_cluster
        )
    preview_map.save("static/preview/preview_map.html")
    return render_template("main/map.html", enable_scroll_nav=False)


# Mengambil data restoran dari API GOOGLE MAPS
# Google Maps Client
gmaps = googlemaps.Client(key=app.config["GOOGLE_API_KEY"])


@app.route("/fetch_google_maps", methods=["GET"])
def fetch_google_maps():
    # Koordinat dan radius pencarian
    semarang_location = {"lat": -7.005145, "lng": 110.438125}

    radius = 60000  # mengambil data restoran dalam satuan meter dari koordinat

    places_result = gmaps.places_nearby(
        location=semarang_location,
        radius=radius,
        type="restaurant",
    )

    for place in places_result.get("results", []):
        name = place.get("name")
        lat = place["geometry"]["location"]["lat"]
        lon = place["geometry"]["location"]["lng"]
        img_url = None
        if place.get("photos"):
            photo_reference = place["photos"][0]["photo_reference"]
            img_url = (
                f"https://maps.googleapis.com/maps/api/place/photo"
                f"?maxwidth=400&photoreference={photo_reference}&key={app.config['GOOGLE_API_KEY']}"
            )
        price_range = place.get("price_level", "Tidak diketahui")
        desc = ", ".join(place.get("types", []))

        # Simpan ke database
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
    flash("Data restoran dari Google Maps berhasil ditambahkan ke database.")
    return redirect(url_for("map"))


if __name__ == "__main__":
    app.run(debug=True)
