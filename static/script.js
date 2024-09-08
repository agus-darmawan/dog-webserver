function fetchLatestDetection() {
    fetch('/api/deteksi') // Sesuaikan ini jika perlu, misalnya, robot mengirim gambar ke endpoint ini
        .then(response => response.json())
        .then(data => {
            let statusText = document.getElementById('status');
            let detectedImage = document.getElementById('detectedImage');
            let timestampText = document.getElementById('timestamp');

            // Update konten halaman
            statusText.textContent = data.message;
            detectedImage.src = data.image_url;
            detectedImage.style.display = 'block';
            timestampText.textContent = "Waktu Deteksi: " + data.timestamp;
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

// Jalankan fetchLatestDetection setiap 5 detik
setInterval(fetchLatestDetection, 5000);
