# CARA MENJALANKAN PROJECT

1. Clone project di directory yang di pilih dengan perintah "git clone" atau bisa manual
   ```
   git clone https://github.com/zeys0/SIG-Kuliner-Semarang.git
   ```
   
3. Masuk ke dalam file yg telah di clone
   
5. Buat folder venv dengan perintah pada powershell
   ```
   python -m venv venv
   ```
   
7. Lalu ketikkan perintah
   ```
   .\venv\scripts\activate
   ```
   
9. jika terjadi error execution policy, konfiguarsi dlu pada setting json dengan perintah "ctrl + p" lalu ketik ">" dan cari file setting json lalu copy code berikut didalam setting json
   (Jika tidak error skip bagian ini)
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
   
11. Install library berikut dengan perintah
   ```
   pip install flask folium flask-migrate flask-sqlalchemy
   ```
    
12. Run app.py
   
