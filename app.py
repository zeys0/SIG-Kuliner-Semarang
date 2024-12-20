import json
import folium
from flask import Flask, render_template, request, redirect, url_for, flash
from folium.plugins import MarkerCluster
from flask_migrate import Migrate
from models import db, Place


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

preview_map.save("static/preview/preview_map.html")


@app.route("/")
def home():
    return render_template("main/home.html", enable_scroll_nav=True)


@app.route("/map", methods=["GET", "POST"])
def map():
    # ADD DATAS  RESTORAN
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

    # MENAMPILKAN DATA YG DI INPUT PADA PREVIEW MAP
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
    return render_template("main/map.html", enable_scroll_nav=False, places=places)


def update_preview_map():

    updated_map = folium.Map(location=[-7.011374, 110.395078], zoom_start=12)

    marker_cluster = MarkerCluster().add_to(updated_map)
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

    updated_map.save("static/preview/preview_map.html")


# DELETE DATA
@app.route("/delete", methods=["POST"])
def delete_place():
    place_id = request.form["place_id"]  # mengambil ID tempat dari form
    place = Place.query.get(place_id)  # Menuliskan query data berdasarkan ID
    if place:
        db.session.delete(place)
        db.session.commit()
        flash(f"Data {place.name} berhasil dihapus.")
        # Memperbarui ulang peta setelah menghapus data
        update_preview_map()
    else:
        flash("Data tidak ditemukan.")
    return redirect(url_for("map"))


# # UNTUK MENGHAPUS SELURUH DATA DARI DB
# @app.cli.command("delete_all_data")
# def delete_all_data():
#     """Menghapus semua data dari tabel."""
#     db.session.query(Place).delete()
#     db.session.commit()
#     print("Semua data berhasil dihapus.")


# UNTUK MERESET DATA DARI DB
# @app.cli.command("reset_database")
# def reset_database():
#     """Menghapus seluruh tabel dan datanya."""
#     db.drop_all()  # Menghapus semua tabel
#     db.create_all()  # Membuat ulang tabel sesuai model
#     print("Database berhasil di-reset.")


if __name__ == "__main__":
    app.run(debug=True)
