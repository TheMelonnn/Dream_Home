# DreamHome Project

DreamHome adalah aplikasi web yang dirancang untuk membantu pengguna merencanakan dan mengelola biaya perabotan untuk rumah impian mereka. Pengguna dapat membuat "ruangan" virtual, mencari produk dari berbagai toko online, menambahkannya ke ruangan mereka, dan secara otomatis mengakumulasi total biaya untuk setiap ruangan.

![Logo Aplikasi DreamHome](themelonnn/dream_home/Dream_Home-8b31b21f7baf43662742524124d48dbb8037f599/static/image/applogo.png)

## Fitur Utama

* **Manajemen Ruangan**: Pengguna dapat membuat beberapa ruangan (misalnya, "Kamar Tidur Utama", "Dapur", "Ruang Tamu") dan menghapusnya.
* **Web Scraping Produk**: Aplikasi dapat mengambil detail produk (nama, harga, dan gambar) secara *real-time* dari berbagai situs e-commerce.
    * Toko yang Didukung: IKEA, RupaRupa, dan UFO Elektronika.
* **Kalkulasi Biaya Otomatis**: Secara otomatis menghitung total biaya perabotan untuk setiap ruangan berdasarkan harga dan kuantitas produk yang ditambahkan.
* **Database Produk**: Menyimpan produk yang telah di-crawl ke dalam database SQLite, menautkannya ke ruangan tertentu.
* **Antarmuka Web Sederhana**: UI yang bersih dan responsif untuk navigasi, menambah ruangan, dan melihat produk.

## Teknologi yang Digunakan

* **Backend**: Python, Flask
* **Database**: SQLite 3
* **Web Scraping**: `requests`, `BeautifulSoup`
* **Frontend**: HTML5, CSS3 (dengan template Jinja2)

## Syarat Instalasi

Sebelum menjalankan proyek ini, pastikan Anda telah menginstal *library* Python yang diperlukan.

1.  **Clone repository ini:**
    ```bash
    git clone [https://github.com/themelonnn/dream_home.git](https://github.com/themelonnn/dream_home.git)
    cd dream_home
    ```

2.  **Buat dan aktifkan virtual environment (direkomendasikan):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Pada Windows: venv\Scripts\activate
    ```

3.  **Install dependensi:**
    Tertulis di requirements.txt
    ```bash
    pip install Flask requests beautifulsoup4 lxml
    ```

4.  **Inisialisasi database:**
    Jalankan skrip `createdb.py` untuk membuat file `database.db` dan tabel yang diperlukan.
    ```bash
    python createdb.py
    ```

5.  **Jalankan aplikasi:**
    ```bash
    flask run
    # atau
    python main.py
    ```
    Aplikasi akan berjalan di `http://127.0.0.1:5000`.

## Susunan Project
Dream_Home/ ├── createdb.py # Skrip untuk inisialisasi database SQLite ├── database.db # File database (dibuat oleh createdb.py) ├── main.py # File utama aplikasi Flask (routing dan logika utama) ├── webcrawling.py # Modul untuk fungsi web scraping ├── pycache/ # Direktori cache Python ├── static/ │ └── image/ │ ├── applogo.png │ ├── getstartedhero.jpg │ └── hero.jpg └── templates/ ├── add-product.html # Halaman untuk menambah produk via link ├── dashboard.html # Halaman dashboard utama (daftar ruangan) ├── home.html # Halaman landing/beranda └── room.html # Halaman detail untuk satu ruangan (daftar produk)

## Contoh Penggunaan

1.  **Buka Aplikasi**: Akses `http://127.0.0.1:5000` di browser Anda.
2.  **Masuk ke Dashboard**: Klik tombol "Get Started" atau "Dashboard".
3.  **Tambah Ruangan**: Di halaman Dashboard, gunakan tombol `+` untuk membuka form. Masukkan nama ruangan (misal: "Kamar Tidur") dan klik "Add". Ruangan baru akan muncul di daftar.
4.  **Masuk ke Ruangan**: Klik nama ruangan yang baru Anda buat.
5.  **Tambah Produk**:
    * Klik tombol `+` di halaman ruangan untuk pergi ke halaman "Add Product".
    * Cari produk di situs IKEA, RupaRupa, atau UFO Elektronika.
    * Salin (copy) URL produk tersebut.
    * Tempel (paste) URL ke dalam form "Enter Product Link".
    * Pilih sumber (Source) yang benar (IKEA, RupaRupa, dll).
    * Klik "Crawl".
6.  **Simpan Produk**: Aplikasi akan menampilkan preview produk (gambar, nama, harga). Klik "Save Product" untuk menambahkannya ke ruangan Anda.
7.  **Lihat Total Biaya**: Kembali ke halaman ruangan. Produk Anda akan terdaftar dan total biaya ruangan akan diperbarui secara otomatis.