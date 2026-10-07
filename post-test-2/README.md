# Posttest 2 - Pemrograman Berorientasi Objek

## Audiophile HS Store: Relasi UML & Inheritance

## 1. Deskripsi Program

Program ini adalah simulasi sistem toko perangkat audio **Audiophile HS Store** yang menjual **IEM** (in-ear monitor) dan **DAC** (Digital-to-Analog Converter). Program ini merupakan lanjutan dari Posttest 1 dengan judul yang sama.

Fitur utama program:

- Mengelola produk IEM dan DAC lengkap dengan stok, harga, dan spesifikasi masing-masing.
- Menampilkan katalog produk toko.
- Konsultasi daya: pelanggan mengecek apakah IEM pilihannya perlu ditambah DAC, berdasarkan impedansi.
- Keranjang belanja dan checkout dengan diskon member serta pengecekan saldo.
- Validasi data lewat getter dan setter (stok, harga, saldo).

Perbedaan dengan Posttest 1:

| Aspek | Posttest 1 | Posttest 2 |
|---|---|---|
| Struktur produk | `IEM` dan `DAC` berdiri sendiri, atribut diulang | `IEM` dan `DAC` mewarisi superclass `Produk` |
| Class baru | - | `Produk`, `Toko`, `Keranjang` |
| Relasi antar class | Hanya penggunaan objek lewat parameter | Asosiasi, Agregasi, dan Komposisi |
| Hak akses | Public dan private | Public, protected, dan private pada pewarisan |

## 2. Struktur Class

### 2.1 Class `Produk` (Superclass)

Class induk yang menyimpan data dan perilaku yang sama untuk semua produk.

| Anggota | Jenis | Keterangan |
|---|---|---|
| `nama_toko`, `total_produk`, `garansi_standar_bulan` | Atribut class | Data milik class, dipakai bersama semua objek |
| `merk`, `nama_model` | Atribut public | Identitas produk |
| `_harga`, `_stok` | Atribut protected | Boleh diakses dan diubah langsung oleh subclass |
| `__harga_modal` | Atribut private | Rahasia superclass, hanya bisa dibaca lewat `hitung_margin()` |
| `tambah_total_produk()` | Class method | Menambah penghitung `total_produk` |
| `validasi_nama_merk(nama)` | Static method | Mengecek nama berupa string tidak kosong |
| `harga`, `stok` | Property (getter/setter) | Setter memvalidasi: harga harus integer lebih dari 0, stok harus integer tidak negatif |
| `hitung_margin()` | Method | Mengembalikan `_harga - __harga_modal` |
| `info_garansi()` | Method | Garansi toko 6 bulan (akan di-override) |
| `tampilkan_info()` | Method | Menampilkan merk, model, harga, stok (akan di-override) |

### 2.2 Class `IEM` (Subclass)

| Anggota | Jenis | Keterangan |
|---|---|---|
| `impedansi`, `jenis_driver` | Atribut unik | Hanya dimiliki `IEM` |
| `batas_impedansi_berat` | Atribut class | Batas 50 Ohm untuk menentukan IEM berat |
| `butuh_dac()` | Method | `True` bila impedansi melebihi batas |
| `restock(jumlah)` | Method | Menambah `_stok` secara langsung (memakai atribut protected) |
| `tampilkan_info()` | Override | Memanggil `super().tampilkan_info()` lalu menambah impedansi dan driver |

### 2.3 Class `DAC` (Subclass)

| Anggota | Jenis | Keterangan |
|---|---|---|
| `power_output`, `jenis_koneksi` | Atribut unik | Hanya dimiliki `DAC` |
| `garansi_dac_bulan` | Atribut class | Garansi DAC 12 bulan |
| `buat_dari_string(data_string)` | Class method | Membuat objek DAC dari string dengan format `merk,model,harga,stok,modal,power,koneksi` |
| `hitung_estimasi_cicilan(harga_barang, bulan)` | Static method | Harga dibagi jumlah bulan |
| `terapkan_promo_bundling(persen)` | Method | Mengubah `_harga` secara langsung (memakai atribut protected) |
| `info_garansi()` | Override | Mengembalikan garansi 12 bulan, berbeda dari `Produk` |
| `tampilkan_info()` | Override | Memanggil `super().tampilkan_info()` lalu menambah output dan koneksi |

### 2.4 Class `Keranjang`

Menyimpan produk yang dipilih pelanggan di atribut private `__daftar_produk`. Properti `daftar_produk` mengembalikan salinan list agar isi aslinya tidak bisa diubah dari luar. Method `hitung_total()` menjumlahkan harga semua produk, `kosongkan()` mengosongkan keranjang, dan `tampilkan_isi()` mencetak isinya.

### 2.5 Class `Toko`

Menyimpan katalog di atribut private `__katalog`. Method `tambah_produk()` menerima objek `Produk` yang dibuat di luar class, dan `tampilkan_katalog()` memanggil `tampilkan_info()` milik tiap produk. Karena method itu di-override, setiap jenis produk tampil dengan format berbeda (polimorfisme).

### 2.6 Class `Pelanggan`

| Anggota | Jenis | Keterangan |
|---|---|---|
| `total_pelanggan`, `diskon_member` | Atribut class | Penghitung pelanggan dan diskon member (default 10%) |
| `nama`, `perangkat_pemutar` | Atribut public | Data pelanggan |
| `__saldo` | Atribut private | Diakses lewat property `saldo` dengan validasi tidak boleh negatif |
| `keranjang` | Atribut objek | Instance `Keranjang` yang dibuat di constructor |
| `ubah_diskon_member(diskon_baru)` | Class method | Mengubah diskon untuk semua pelanggan |
| `cek_kelayakan_beli(saldo, harga_barang)` | Static method | `True` bila saldo mencukupi |
| `konsultasi_daya(objek_iem)` | Method | Menyarankan DAC atau tidak berdasarkan `butuh_dac()` |
| `tambah_ke_keranjang(produk)` | Method | Menambah produk bila stok masih ada |
| `checkout()` | Method | Menghitung total, menerapkan diskon, mengecek saldo, mengurangi stok dan saldo |

## 3. Penerapan Relasi UML

| Relasi | Class | Penjelasan | Letak di kode |
|---|---|---|---|
| Asosiasi | `Pelanggan` dan `Produk` (`IEM`) | `Pelanggan` hanya menggunakan objek produk lewat parameter method. Tidak ada kepemilikan, dan kedua objek hidup sendiri-sendiri. | `Pelanggan.konsultasi_daya(objek_iem)`, `Pelanggan.tambah_ke_keranjang(produk)` |
| Agregasi | `Toko` dan `Produk` | `Toko` menyimpan daftar produk, tetapi produk dibuat di luar `Toko` lalu dimasukkan. Jika `Toko` dihapus, produk tetap ada. | `Toko.tambah_produk(produk)` dan `del toko` di akhir `main` |
| Komposisi | `Pelanggan` dan `Keranjang` | `Keranjang` dibuat di dalam constructor `Pelanggan`, sehingga siklus hidupnya mengikuti pemiliknya dan tidak punya arti tanpa pelanggan. | `self.keranjang = Keranjang()` di `Pelanggan.__init__` |

Cara membedakan: pada agregasi objek bagian dibuat **di luar** dan dilewatkan ke objek induk, sedangkan pada komposisi objek bagian dibuat **di dalam** objek induk.

## 4. Penerapan Inheritance

| Ketentuan | Penerapan |
|---|---|
| Superclass minimal 1 | `Produk` |
| Subclass minimal 2 | `IEM` dan `DAC` |
| `super().__init__(...)` | Dipanggil di constructor `IEM` dan `DAC` |
| Atribut unik tiap subclass | `IEM`: `impedansi`, `jenis_driver`. `DAC`: `power_output`, `jenis_koneksi` |
| Method overriding | `tampilkan_info()` di `IEM` dan `DAC`, serta `info_garansi()` di `DAC` |
| Protected | `_harga` dan `_stok`, diubah langsung di `DAC.terapkan_promo_bundling()` dan `IEM.restock()` |
| Private | `__harga_modal`, hanya diakses lewat `Produk.hitung_margin()` |

Potongan kode constructor subclass:

```python
class IEM(Produk):
    def __init__(self, merk, nama_model, harga, stok, harga_modal, impedansi, jenis_driver):
        super().__init__(merk, nama_model, harga, stok, harga_modal)
        self.impedansi = impedansi
        self.jenis_driver = jenis_driver
```

Potongan kode method overriding:

```python
class DAC(Produk):
    def info_garansi(self):
        return f"Garansi resmi DAC {DAC.garansi_dac_bulan} bulan (lebih panjang dari garansi toko)"
```

Catatan tentang private: atribut `__harga_modal` mengalami name mangling menjadi `_Produk__harga_modal`, sehingga `iem2.__harga_modal` dari luar class menghasilkan `AttributeError`. Subclass juga tidak bisa membacanya langsung dengan nama itu, karena itu `hitung_margin()` didefinisikan di `Produk`.

## 5. Alur Program

Program dijalankan dari blok `if __name__ == "__main__"` dengan urutan berikut:

1. Membuat dua objek `IEM` (`iem1`, `iem2`) dan dua objek `DAC` (`dac1` lewat constructor, `dac2` lewat `DAC.buat_dari_string`).
2. Membuat objek `Toko` dan memasukkan keempat produk ke katalog (agregasi).
3. Membuat dua `Pelanggan`, yang masing-masing otomatis memiliki `Keranjang` (komposisi).
4. Menampilkan katalog, lalu menguji pewarisan dan overriding lewat `info_garansi()` dan `isinstance()`.
5. Pelanggan melakukan konsultasi daya terhadap IEM (asosiasi).
6. Pelanggan mengisi keranjang dan melakukan checkout.
7. Menguji atribut protected (`restock`, promo bundling) dan private (`hitung_margin`, akses langsung gagal).
8. Menguji class method, static method, getter, setter, dan validasi.
9. Menghapus objek `toko` untuk membuktikan produk tetap ada.

## 6. Panduan Pengujian

### 6.1 Persiapan

- Python 3.8 atau lebih baru (tidak butuh library tambahan).
- Simpan `main.py` di satu folder.

### 6.2 Cara Menjalankan

```bash
python main.py
```

Bila Python 3 terpasang dengan nama berbeda:

```bash
python3 main.py
```

### 6.3 Skenario Pengujian

Tiap skenario sesuai satu bagian pada output program (judul dalam tanda kurung siku).

| No | Skenario | Bagian Output | Hasil yang Diharapkan |
|---|---|---|---|
| 1 | Agregasi: produk dimasukkan ke toko | `[UJI AGREGASI]` | Jumlah produk di katalog 4, dan semua produk tampil |
| 2 | Polimorfisme `tampilkan_info()` | `[UJI AGREGASI]` | Baris IEM menampilkan impedansi dan driver, baris DAC menampilkan output dan koneksi |
| 3 | Method overriding `info_garansi()` | `[UJI INHERITANCE & METHOD OVERRIDING]` | IEM: garansi toko 6 bulan. DAC: garansi resmi 12 bulan |
| 4 | Pengecekan tipe | `[UJI INHERITANCE & METHOD OVERRIDING]` | `iem1` dan `dac1` adalah `Produk` (True), `iem1` bukan `DAC` (False) |
| 5 | Asosiasi: konsultasi IEM ringan | `[UJI ASOSIASI]` | Hammam dengan Wyvern Celest (32 Ohm) mendapat hasil RINGAN |
| 6 | Asosiasi: konsultasi IEM berat | `[UJI ASOSIASI]` | Syamil dengan IE200 (60 Ohm) mendapat hasil BERAT dan disarankan membeli DAC |
| 7 | Komposisi: checkout berhasil | `[UJI KOMPOSISI]` | Hammam membayar Rp315.000 (350.000 dikurangi diskon 10%), stok Wyvern Celest turun dari 10 ke 9, sisa saldo Rp185.000 |
| 8 | Checkout gagal karena saldo kurang | `[UJI KOMPOSISI]` | Syamil dengan total setelah diskon Rp3.870.000 dan saldo Rp3.000.000 mendapat pesan GAGAL, stok dan saldo tidak berubah |
| 9 | Protected: stok diubah subclass | `[UJI ATRIBUT PROTECTED]` | `restock(5)` menambah stok Wyvern Celest dari 9 menjadi 14 |
| 10 | Protected: harga diubah subclass | `[UJI ATRIBUT PROTECTED]` | Promo 10% menurunkan harga BTR15 dari Rp1.800.000 menjadi Rp1.620.000 |
| 11 | Private: akses lewat method | `[UJI ATRIBUT PRIVATE]` | `hitung_margin()` IE200 bernilai Rp400.000 |
| 12 | Private: akses langsung | `[UJI ATRIBUT PRIVATE]` | Muncul pesan `AttributeError` |
| 13 | Class method dan static method | `[UJI CLASS METHOD & STATIC METHOD]` | Total produk 4, total pelanggan 2, diskon member menjadi 15%, cicilan BTR15 6 bulan Rp270.000 (dari harga setelah promo, Rp1.620.000) |
| 14 | Validasi input salah | `[UJI GETTER, SETTER & VALIDASI]` | Stok negatif, stok bukan angka, harga 0, dan saldo negatif semuanya ditolak dengan pesan `[Validasi Gagal]` |
| 15 | Validasi input benar | `[UJI GETTER, SETTER & VALIDASI]` | Stok 15, harga Rp1.700.000, dan saldo Rp800.000 diterima dengan pesan `[Validasi Sukses]` |
| 16 | Bukti agregasi | `[BUKTI AGREGASI]` | Setelah `del toko`, `iem1` masih bisa diakses |

### 6.4 Pengujian Manual Tambahan

Tambahkan baris berikut di bagian bawah blok `main` untuk mencoba kasus lain, lalu jalankan ulang.

Produk dengan stok habis tidak bisa masuk keranjang:

```python
iem1.stok = 0
pel2.tambah_ke_keranjang(iem1)
```

Hasil: muncul `[Gagal] Wyvern Celest sedang habis.`

Validasi nama merk:

```python
print(Produk.validasi_nama_merk(""))
print(Produk.validasi_nama_merk("Fiio"))
```

Hasil: `False` lalu `True`.

Mengisi saldo agar checkout Syamil berhasil:

```python
pel2.saldo = 5000000
pel2.checkout()
```

Hasil: pembayaran berhasil, stok IE200 dan BTR15 masing-masing berkurang 1, keranjang kosong.

## 7. Output Program

Output berikut adalah hasil nyata dari menjalankan `python main.py`.

```text
=== Selamat Datang di Audiophile HS Store ===

[UJI AGREGASI: Toko memiliki Produk]
Jumlah produk di katalog: 4
[KATALOG AUDIOPHILE HS STORE]
Kinera Wyvern Celest | Rp350000 | Stok: 10
   -> Tipe: IEM | Impedansi: 32 Ohm | Driver: Dynamic Driver
Sennheiser IE200 | Rp2500000 | Stok: 5
   -> Tipe: IEM | Impedansi: 60 Ohm | Driver: Dynamic Driver
Fiio BTR15 | Rp1800000 | Stok: 8
   -> Tipe: DAC | Output: 340mW | Koneksi: Bluetooth
Moondrop DawnPro | Rp800000 | Stok: 4
   -> Tipe: DAC | Output: 120mW | Koneksi: USB-C

[UJI INHERITANCE & METHOD OVERRIDING]
Garansi IEM : Garansi toko 6 bulan
Garansi DAC : Garansi resmi DAC 12 bulan (lebih panjang dari garansi toko)
isinstance(iem1, Produk) = True
isinstance(dac1, Produk) = True
isinstance(iem1, DAC)    = False

[UJI ASOSIASI: Pelanggan menggunakan IEM]

--- Sesi Konsultasi: Hammam ---
Perangkat Anda: Samsung Galaxy A13
Target IEM    : Kinera Wyvern Celest (Impedansi: 32 Ohm)
>> HASIL: IEM ini RINGAN. Bisa langsung dicolok ke HP/Laptop Anda tanpa masalah daya.

--- Sesi Konsultasi: Syamil ---
Perangkat Anda: Laptop Asus VivoBook
Target IEM    : Sennheiser IE200 (Impedansi: 60 Ohm)
>> HASIL: IEM ini BERAT. HP/Laptop Anda mungkin tidak kuat. Sangat disarankan membeli DAC tambahan!

[UJI KOMPOSISI: Pelanggan memiliki Keranjang]
[Keranjang Hammam] Wyvern Celest ditambahkan.
[Keranjang Syamil] IE200 ditambahkan.
[Keranjang Syamil] BTR15 ditambahkan.

--- Checkout: Hammam ---
   1. Kinera Wyvern Celest - Rp350000
   Total: Rp350000 | Setelah diskon member: Rp315000
[Validasi Sukses] Stok Wyvern Celest berhasil diubah menjadi 9.
>> Pembayaran berhasil. Sisa saldo Hammam: Rp185000

--- Checkout: Syamil ---
   1. Sennheiser IE200 - Rp2500000
   2. Fiio BTR15 - Rp1800000
   Total: Rp4300000 | Setelah diskon member: Rp3870000
>> Pembayaran GAGAL. Saldo Syamil (Rp3000000) tidak cukup.

[UJI ATRIBUT PROTECTED DI SUBCLASS]
[Restock] Stok Wyvern Celest bertambah 5, sekarang 14.
[Promo] Harga BTR15 turun 10% menjadi Rp1620000.

[UJI ATRIBUT PRIVATE DI SUPERCLASS]
Margin IE200 via method superclass: Rp400000
Akses langsung ke __harga_modal dari luar class -> AttributeError

[UJI CLASS METHOD & STATIC METHOD]
Total produk terdaftar: 4
Total pelanggan: 2
Diskon member untuk semua pelanggan diubah menjadi 15.0%
Estimasi cicilan DAC Fiio BTR15 selama 6 bulan: Rp 270000.0
Validasi nama merk 'Fiio': True

[UJI GETTER, SETTER & VALIDASI]
>> Menguji input SALAH:
[Validasi Gagal] Stok Wyvern Celest tidak boleh negatif!
[Validasi Gagal] Stok Wyvern Celest harus berupa angka!
[Validasi Gagal] Harga BTR15 harus angka lebih dari 0!
[Validasi Gagal] Saldo Hammam tidak boleh negatif!

>> Menguji input BENAR:
[Validasi Sukses] Stok Wyvern Celest berhasil diubah menjadi 15.
[Validasi Sukses] Harga BTR15 berhasil diubah menjadi Rp1700000.
[Validasi Sukses] Saldo Hammam berhasil diisi.

>> Cek data setelah diupdate via Getter:
Stok akhir Wyvern Celest = 15
Harga akhir BTR15 = Rp1700000
Saldo akhir Hammam = Rp800000

[BUKTI AGREGASI: Produk tetap ada walau Toko dihapus]
Toko dihapus, produk masih ada: Kinera Wyvern Celest
```