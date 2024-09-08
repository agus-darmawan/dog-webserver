import os
from flask import Flask, request, render_template, jsonify, send_from_directory
from flask_cors import CORS  # Tambahkan ini
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Tambahkan ini untuk mengizinkan permintaan lintas domain
app.config['UPLOAD_FOLDER'] = 'uploads/'
# Membuat folder upload jika belum ada

# Membuat folder upload jika belum ada
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Variabel untuk menyimpan gambar terakhir dan timestamp
last_image = None
last_timestamp = None

# API untuk menerima gambar dan timestamp dari robot
@app.route('/api/deteksi', methods=['POST'])
def deteksi_korban():
    global last_image, last_timestamp
    
    if 'image' not in request.files:
        return jsonify({"error": "Tidak ada file gambar yang dikirim"}), 400
    
    image = request.files['image']
    timestamp = request.form.get('timestamp', datetime.now().isoformat())

    if image.filename == '':
        return jsonify({"error": "Tidak ada file yang dipilih"}), 400

    filename = secure_filename(image.filename)
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image.save(image_path)

    # Menyimpan informasi gambar terakhir dan timestamp
    last_image = filename

    # Mengubah format timestamp menjadi DD-MM-YYYY HH:MM:SS
    last_timestamp = datetime.fromisoformat(timestamp).strftime('%d-%m-%Y %H:%M:%S')

    return jsonify({
        "message": "Gambar berhasil diterima",
        "image_url": f"/uploads/{filename}",
        "timestamp": last_timestamp
    })

# Endpoint untuk menampilkan gambar terakhir dan timestamp di frontend
@app.route('/')
def index():
    global last_image, last_timestamp
    
    # Jika belum ada gambar yang diunggah
    if last_image is None:
        return render_template('index.html', image_url=None, timestamp=None)
    
    # Kirim informasi gambar terakhir dan timestamp ke halaman
    return render_template('index.html', image_url=f'/uploads/{last_image}', timestamp=last_timestamp)

# Menyajikan gambar yang diunggah
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
