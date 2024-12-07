# CARA MENJALANKAN PROJECT

1. Clone project di directory yang di pilih dengan perintah "git clone" atau bisa manual
   ```
   git clone https://github.com/zeys0/SIG-Kuliner-Semarang.git
   ```
   
2. Masuk ke dalam file yg telah di clone
   
3. Buat folder venv dengan perintah seperti di bawah pada powershell
   ```
   python -m venv venv
   ```
   
4. Lalu ketikkan perintah pada powershell
   ```
   .\venv\scripts\activate
   ```
   
5. jika terjadi error execution policy, konfiguarsi dlu pada setting json dengan perintah "ctrl + p" lalu ketik ">" dan cari file setting json lalu copy code berikut didalam setting json
   (Jika tidak error skip bagian 5 dan 6)
   ```"terminal.integrated.profiles.windows": {
        "PowerShell": {
            "source": "PowerShell",
            "icon": "terminal-powershell",
            "args": [
                "-ExecutionPolicy",
                "Bypass"
            ]
        }
    }
   ```
6. Setelah itu kembali ke powershell dan ketikkan perintah pada nomor 6
   
7. Lalu Install library berikut dengan perintah
   ```
   pip install flask folium flask-migrate flask-sqlalchemy
   ```
    
8. Run app.py
   
