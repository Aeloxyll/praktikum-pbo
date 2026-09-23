 Posttest 1 PBO: Sistem Toko Audio & Konsultasi (IEM & DAC)

 Penjelasan Program
Program ini adalah simulasi sederhana dari sistem manajemen di toko perangkat audio high-fidelity. Program dibuat menggunakan bahasa Python. Fitur utamanya bukan sekadar menyimpan data barang (IEM dan DAC), tetapi juga memiliki fitur Konsultasi Daya. Di sini, objek pelanggan dapat berinteraksi dengan objek IEM untuk mengecek apakah spesifikasi (Impedansi/Ohm) dari IEM tersebut cocok untuk dicolok langsung ke HP/Laptop pelanggan, atau butuh amplifier (DAC) tambahan.

 Struktur Class
 1. Class `IEM` (In-Ear Monitor)
Berfungsi menyimpan data produk earphone.
- Atribut: Memiliki atribut kelas (`nama_toko`, dsb), atribut public (`merk`, `impedansi`), dan atribut private (`__stok`, `__harga`).
- Method: 
  - `tampilkan_info()` (Instance Method)
  - `tambah_total_iem()` (Class Method)
  - `validasi_nama_merk()` (Static Method)
- Encapsulation: Menggunakan `@property` dan `@stok.setter` untuk memvalidasi agar stok tidak bisa diisi dengan huruf atau angka negatif.
 2. Class `DAC` (Digital-to-Analog Converter)
Berfungsi menyimpan data produk amplifier.
- Atribut: Menyimpan data spesifikasi daya output DAC dan harganya secara private.
- Method: Menampilkan Factory Method melalui `@classmethod buat_dari_string()` yang memungkinkan pembuatan objek baru hanya dari input teks string (misal: `"Merk-Model-Power-Harga"`).
- Encapsulation: Menggunakan getter & setter untuk memvalidasi perubahan harga barang.
 3. Class `Pelanggan`
Berfungsi menyimpan data user dan menangani logika interaksi.
- Atribut: Menyimpan nama, perangkat pemutar bawaan, dan saldo private.
- Method Utama: `konsultasi_daya(self, objek_iem)`. Ini adalah Instance Method di mana objek pelanggan membandingkan spesifikasi perangkatnya dengan nilai impedansi dari objek IEM yang dilempar sebagai parameter.

Panduan Pengujian
Untuk menguji program ini, jalankan langsung file Python di terminal dengan command `python nama_file_kamu.py`. Pada bagian bawah program akan menghasilkan output berdasarkan pengujian, dengan urutan pengujian:
- Uji Instance Method (Katalog & Konsultasi)
  Fungsi `tampilkan_info()` dipanggil untuk mencetak ringkasan seluruh produk di katalog. Setelah itu, Pelanggan bernama Hammam dan Syamil melakukan simulasi `konsultasi_daya()`. Hammam mengecek kecocokan IEM Kinera (ringan) yang berhasil, sedangkan Syamil mengecek IEM Sennheiser (berat) dan sistem merespons dengan saran untuk membeli DAC tambahan.
- Uji Class Method
  Program memunculkan total objek yang terdaftar, lalu menggunakan fungsi `ubah_diskon_member()` untuk mengubah diskon toko menjadi 15%. Karena menggunakan `@classmethod`, nilai diskon ini otomatis berubah untuk keseluruhan pelanggan di dalam sistem.
- Uji Static Method
  Program akan memanggil `cek_kelayakan_beli()` untuk mengecek apakah saldo milik Syamil mencukupi untuk membeli IEM Sennheiser, dan output menampilkan status True. Terdapat juga pengujian perhitungan estimasi cicilan DAC selama 6 bulan menggunakan fungsi `hitung_estimasi_cicilan()`.
- Uji Encapsulation (Getter & Setter)
  - Uji validasi setter dilakukan dengan sengaja memasukkan nilai stok negatif `-5`, teks `"Kosong"`, serta saldo negatif. Sesuai aturan validasi data di dalam setter, percobaan ini ditolak dan program memunculkan pesan peringatan `[Validasi Gagal]` tanpa membuat program crash.
  - Setelah itu, nilai stok dan saldo diubah dengan data yang benar (valid).
  - Terakhir, Getter akan dipanggil untuk mengambil dan mencetak status nilai stok serta saldo yang terbaru.