import json
import folium
from flask import Flask, render_template, request, redirect, url_for, flash
from folium.plugins import MarkerCluster
from flask_migrate import Migrate
import googlemaps
import os
from dotenv import load_dotenv
from os.path import join, dirname
from pymongo import MongoClient, DESCENDING
from bson import ObjectId

app = Flask(__name__)
dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

# Mengambil data restoran dari API GOOGLE MAPS
# Google Maps Client
app.config["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
gmaps = googlemaps.Client(key=app.config["GOOGLE_API_KEY"])

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME = os.environ.get("DB_NAME")
SECRET_KEY = os.environ.get("SECRET_KEY")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]
app.secret_key = SECRET_KEY
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
    return render_template("main/home.html", enable_scroll_nav=False)


@app.route("/map", methods=["GET", "POST"])
def map():
    # ADD DATA RESTORAN
    if request.method == "POST":
        name = request.form["name"]
        lat = float(request.form["lat"])
        lon = float(request.form["lon"])
        img_url = request.form["img_url"]
        price_range = request.form["price_range"]
        desc = request.form["desc"]

        new_place = {
            "name": name,
            "lat": lat,
            "lon": lon,
            "image_url": img_url,
            "price_range": price_range,
            "description": desc,
        }

        db.places.insert_one(new_place)  # Menambahkan data ke MongoDB
        flash("Berhasil Menambah data")
        return redirect(url_for("map"))

    # MENAMPILKAN DATA YG DI INPUT PADA PREVIEW MAP
    marker_cluster = MarkerCluster().add_to(preview_map)
    places = list(db.places.find())  # Mengambil semua data dari MongoDB

    for place in places:
        popup_content = f"""
    <div style="font-family: Arial, sans-serif; width: 300px; padding: 10px; border-radius: 10px; box-shadow: 0px 4px 10px rgba(0,0,0,0.2); background-color: #f9f9f9;">
        <div style=" margin-bottom: 10px;">
            <h3 style="margin: 0; color: #2c3e50;">{place['name']}</h3>
            <p style="font-size: 14px; color: #7f8c8d;">{place['description']}</p>
        </div>
        <div style="text-align: center; margin-bottom: 10px;">
            <img src="{place['image_url']}" alt="Image of {place['name']}" 
                 style="width: 100%; max-height: 150px; object-fit: cover; border-radius: 8px;">
        </div>
        <div style="margin-top: 10px;">
            <p style="margin: 5px 0; font-size: 14px; color: #34495e;"><b>Rating:</b> ⭐⭐⭐⭐⭐ 5/5</p>
            <p style="margin: 5px 0; font-size: 14px; color: #34495e;"><b>Harga:</b> {place['price_range']}</p>
        </div>
    </div>
    """
        folium.Marker([place["lat"], place["lon"]], popup=popup_content).add_to(
            marker_cluster
        )

    preview_map.save("static/preview/preview_map.html")

    return render_template("main/map.html", enable_scroll_nav=False, places=places)


def update_preview_map():

    updated_map = folium.Map(location=[-7.011374, 110.395078], zoom_start=12)

    marker_cluster = MarkerCluster().add_to(updated_map)
    places = db.places.find()  # Mengambil data dari MongoDB
    for place in places:
        popup_content = f"""
    <div style="font-family: Arial, sans-serif; width: 300px; padding: 10px; border-radius: 10px; box-shadow: 0px 4px 10px rgba(0,0,0,0.2); background-color: #f9f9f9;">
        <div style=" margin-bottom: 10px;">
            <h3 style="margin: 0; color: #2c3e50;">{place['name']}</h3>
            <p style="font-size: 14px; color: #7f8c8d;">{place['description']}</p>
        </div>
        <div style="text-align: center; margin-bottom: 10px;">
            <img src="{place['image_url']}" alt="Image of {place['name']}"
                 style="width: 100%; max-height: 150px; object-fit: cover; border-radius: 8px;">
        </div>
        <div style="margin-top: 10px;">
            <p style="margin: 5px 0; font-size: 14px; color: #34495e;"><b>Rating:</b> ⭐⭐⭐⭐⭐ 5/5</p>
            <p style="margin: 5px 0; font-size: 14px; color: #34495e;"><b>Harga:</b> {place['price_range']}</p>
        </div>
    </div>
    """

        folium.Marker([place["lat"], place["lon"]], popup=popup_content).add_to(
            marker_cluster
        )

    updated_map.save("static/preview/preview_map.html")


# DELETE DATA
@app.route("/delete", methods=["POST"])
def delete_place():
    place_id = request.form["place_id"]  # mengambil ID tempat dari form
    place = db.places.find_one(
        {"_id": ObjectId(place_id)}
    )  # Menuliskan query data berdasarkan ID
    if place:
        db.places.delete_one(
            {"_id": ObjectId(place_id)}
        )  # Menghapus data berdasarkan ID
        flash(f"Data {place['name']} berhasil dihapus.")
        # Memperbarui ulang peta setelah menghapus data
        update_preview_map
    else:
        flash("Data tidak ditemukan.")
    return redirect(url_for("map"))


@app.route("/fetch_google_maps", methods=["GET"])
def fetch_google_maps():
    # Koordinat dan radius pencarian
    semarang_location = {"lat": -7.005145, "lng": 110.438125}

    radius = 70000  # mengambil data restoran dalam satuan meter dari koordinat

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

        # Simpan ke database MongoDB
        db.places.insert_one(
            {
                "name": name,
                "lat": lat,
                "lon": lon,
                "image_url": img_url,
                "price_range": price_range,
                "description": desc,
            }
        )

    flash("Data restoran dari Google Maps berhasil ditambahkan ke database.")
    return redirect(url_for("map"))


if __name__ == "__main__":
    app.run(debug=True)
