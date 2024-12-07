# Ini merupakan source code untuk fetch data restoran dari koordinat semarang menggunakan api google maps
# 1. Untuk menggunakannya pastikan sudah mempunyai key api dari google maps, jika belum daftar terlebih dahulu
# 2. Install library dengan perintah "pip install googlemaps, python-dotenv"
# 3. buat file ".env" dengan directory yang sama pada app.py
# 4. Masukkan key api yang ada pada file .env dengan sintaks seperti ini "GOOGLE_API_KEY=masukkan api key di sini"
# 5. Pindahkan seluruh source code  di bawah pada app.py


import googlemaps
import os
from dotenv import load_dotenv


# load .env
load_dotenv()


# Mengambil data restoran dari API GOOGLE MAPS
# Google Maps Client
app.config["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
gmaps = googlemaps.Client(key=app.config["GOOGLE_API_KEY"])


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
