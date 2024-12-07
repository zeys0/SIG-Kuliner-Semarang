

# CARA MENJALANKAN PROJECT



1. Clone project di directory yang di pilih dengan perintah "git clone https://github.com/zeys0/SIG-Kuliner-Semarang.git" atau bisa manual
   
2. Masuk ke dalam file yg telah di clone
   
3. Buat folder venv dengan perintah "python -m venv venv" pada powershell
   
4. Lalu ketikkan perintah ".\venv\scripts\activate"
   
5. jika terjadi error execution policy, konfiguarsi dlu pada setting json dengan perintah "ctrl + p" lalu ketik ">" dan cari file setting json lalu copy code berikut didalam setting json
   (Jika tidak error skip bagian ini"
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
6. Install library yg dibutuhkan dengan perintah "pip install flask folium flask-migrate flask-sqlalchemy"
    
7. Run app.py
   
