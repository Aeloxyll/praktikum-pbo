# Laporan Posttest 1 Praktikum PBO

## Identitas
- **Nama**: Hammam Syamil
- **NIM**: [Masukkan NIM Kamu]
- **Kelas**: [Masukkan Kelas Kamu]
- **Tema**: Sistem Manajemen Penjualan dan Konsultasi Audio (IEM & DAC)

---

## Deskripsi Program
Program ini adalah aplikasi berbasis *Object-Oriented Programming* (OOP) menggunakan bahasa Python yang menyimulasikan sistem di sebuah toko perangkat audio *high-fidelity*. 

Program ini tidak hanya berfungsi sebagai katalog penyimpanan data barang (IEM dan DAC), tetapi juga memiliki fitur **Konsultasi Daya**. Fitur ini memungkinkan interaksi antar objek, di mana sistem dapat mengecek apakah perangkat pemutar (*smartphone/laptop*) milik pelanggan mampu mengangkat spesifikasi teknis (Impedansi) dari IEM yang diinginkan, atau apakah pelanggan membutuhkan DAC tambahan.

---

## Pemenuhan Syarat Posttest (Modul 1, 2, & 3)

Program ini telah memenuhi seluruh kriteria yang disyaratkan pada Posttest 1:

- [x] **Memiliki Minimal 3 Class**: Terdiri dari class `IEM`, `DAC`, dan `Pelanggan`.
- [x] **Atribut Kelas**: Masing-masing class memiliki minimal 3 atribut kelas (contoh: `nama_toko`, `total_pelanggan`, dll).
- [x] **Atribut Instance (Public & Private)**: Menggunakan konstruktor `__init__` dengan atribut *public* (seperti `merk`) dan atribut *private* (seperti `__stok` dan `__saldo`).
- [x] **3 Jenis Method**:
  - *Instance Method*: `tampilkan_info()`, `konsultasi_daya()`
  - *Class Method*: `tambah_total_iem()`, `buat_dari_string()`
  - *Static Method*: `validasi_nama_merk()`, `hitung_estimasi_cicilan()`
- [x] **Encapsulation (Getter & Setter)**: Menggunakan *decorator* `@property` dan `@nama_properti.setter` yang dilengkapi dengan logika validasi data (mencegah input tipe huruf atau angka negatif).

---

## Struktur Class

### 1. Class `IEM`
Blueprint untuk menyimpan data produk *In-Ear Monitor* (earphone).
- **Atribut Kelas**: `nama_toko`, `total_iem_terdaftar`, `batas_impedansi_berat`
- **Atribut Instance**: `merk`, `nama_model`, `impedansi`, `__stok` (Private), `__harga` (Private)
- **Method**: 
  - `tambah_total_iem()` -> Class Method untuk menghitung total objek yang dibuat.
  - `validasi_nama_merk()` -> Static Method untuk mengecek tipe input teks.
  - `tampilkan_info()` -> Instance Method.
  - `@property stok` -> Getter dan Setter dengan validasi tipe data dan angka nol/negatif.

### 2. Class `DAC`
Blueprint untuk menyimpan data produk *Digital-to-Analog Converter* (Amplifier).
- **Atribut Kelas**: `kategori_barang`, `total_dac_terdaftar`, `garansi_standar_bulan`
- **Atribut Instance**: `merk`, `nama_model`, `power_output`, `__harga` (Private)
- **Method**: 
  - `buat_dari_string()` -> Class Method yang berfungsi sebagai *Factory Method* untuk mencetak objek dari format *string*.
  - `hitung_estimasi_cicilan()` -> Static Method untuk fungsi kalkulator utilitas.
  - `@property harga` -> Getter dan Setter dengan validasi nilai.

### 3. Class `Pelanggan`
Blueprint untuk merepresentasikan pengguna yang berinteraksi dengan sistem dan produk.
- **Atribut Kelas**: `total_pelanggan`, `diskon_member`, `level_member_default`
- **Atribut Instance**: `nama`, `perangkat_pemutar`, `__saldo` (Private)
- **Method Utama (`konsultasi_daya`)**: Mengimplementasikan komunikasi antar objek. Menerima `objek_iem` sebagai parameter dan membandingkan atribut `impedansi` IEM tersebut dengan aturan `batas_impedansi_berat` milik toko.

---

## Cara Penggunaan dan Output Program

Program dieksekusi melalui blok `if __name__ == "__main__":` yang mendemonstrasikan pembuatan objek, pemanggilan method, simulasi interaksi konsultasi, serta uji coba validasi setter (berhasil dan gagal).

**Cuplikan Output Program saat Dijalankan:**
```text
=== Selamat Datang di Audiophile Store Samarinda ===

[KATALOG PRODUK]
IEM: Kinera Wyvern Celest | 32 Ohm | Rp350000 | Stok: 10
IEM: Sennheiser IE200 | 60 Ohm | Rp2500000 | Stok: 5
DAC: Fiio BTR15 | Output: 340mW | Harga: Rp1800000
DAC: Moondrop DawnPro | Output: 120mW | Harga: Rp800000

--- Sesi Konsultasi: Hammam ---
Perangkat Anda: Samsung Galaxy A13
Target IEM    : Kinera Wyvern Celest (Impedansi: 32 Ohm)
>> HASIL: IEM ini RINGAN. Bisa langsung dicolok ke HP/Laptop Anda tanpa masalah daya.

--- Sesi Konsultasi: Budi ---
Perangkat Anda: Laptop Asus VivoBook
Target IEM    : Sennheiser IE200 (Impedansi: 60 Ohm)
>> HASIL: IEM ini BERAT. HP/Laptop Anda mungkin tidak kuat. Sangat disarankan membeli DAC tambahan!

[UJI CLASS METHOD]
Total IEM terdaftar: 2
Total Pelanggan: 2
Diskon member untuk semua pelanggan diubah menjadi 15.0%

[UJI STATIC METHOD]
Cek kelayakan beli IEM2 (Rp2.500.000) dengan saldo Budi (Rp3.000.000): True
Estimasi cicilan DAC Fiio BTR15 selama 6 bulan: Rp 300000.0

[UJI GETTER, SETTER & VALIDASI]
>> Menguji input SALAH:
[Validasi Gagal] Stok Wyvern Celest tidak boleh negatif!
[Validasi Gagal] Stok Wyvern Celest harus berupa angka!
[Validasi Gagal] Saldo Hammam tidak boleh negatif!

>> Menguji input BENAR:
[Validasi Sukses] Stok Wyvern Celest berhasil diubah menjadi 15.
[Validasi Sukses] Saldo Hammam berhasil diisi.

>> Cek data setelah diupdate via Getter:
Stok akhir Wyvern Celest = 15
Saldo akhir Hammam = Rp800000