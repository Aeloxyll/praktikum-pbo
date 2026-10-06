class Produk:
    nama_toko = "Audiophile HS Store"
    total_produk = 0
    garansi_standar_bulan = 6

    def __init__(self, merk, nama_model, harga, stok, harga_modal):
        self.merk = merk
        self.nama_model = nama_model
        self._harga = harga
        self._stok = stok
        self.__harga_modal = harga_modal

        Produk.tambah_total_produk()

    @classmethod
    def tambah_total_produk(cls):
        Produk.total_produk += 1

    @staticmethod
    def validasi_nama_merk(nama):
        return isinstance(nama, str) and len(nama) > 0

    @property
    def harga(self):
        return self._harga

    @harga.setter
    def harga(self, nilai_baru):
        if not isinstance(nilai_baru, int) or nilai_baru <= 0:
            print(f"[Validasi Gagal] Harga {self.nama_model} harus angka lebih dari 0!")
        else:
            self._harga = nilai_baru
            print(f"[Validasi Sukses] Harga {self.nama_model} berhasil diubah menjadi Rp{self._harga}.")

    @property
    def stok(self):
        return self._stok

    @stok.setter
    def stok(self, nilai_baru):
        if not isinstance(nilai_baru, int):
            print(f"[Validasi Gagal] Stok {self.nama_model} harus berupa angka!")
        elif nilai_baru < 0:
            print(f"[Validasi Gagal] Stok {self.nama_model} tidak boleh negatif!")
        else:
            self._stok = nilai_baru
            print(f"[Validasi Sukses] Stok {self.nama_model} berhasil diubah menjadi {self._stok}.")

    def hitung_margin(self):
        return self._harga - self.__harga_modal

    def info_garansi(self):
        return f"Garansi toko {self.garansi_standar_bulan} bulan"

    def tampilkan_info(self):
        print(f"{self.merk} {self.nama_model} | Rp{self._harga} | Stok: {self._stok}")


class IEM(Produk):
    batas_impedansi_berat = 50

    def __init__(self, merk, nama_model, harga, stok, harga_modal, impedansi, jenis_driver):
        super().__init__(merk, nama_model, harga, stok, harga_modal)
        self.impedansi = impedansi
        self.jenis_driver = jenis_driver

    def butuh_dac(self):
        return self.impedansi > IEM.batas_impedansi_berat

    def restock(self, jumlah):
        self._stok += jumlah
        print(f"[Restock] Stok {self.nama_model} bertambah {jumlah}, sekarang {self._stok}.")

    def tampilkan_info(self):
        super().tampilkan_info()
        print(f"   -> Tipe: IEM | Impedansi: {self.impedansi} Ohm | Driver: {self.jenis_driver}")


class DAC(Produk):
    garansi_dac_bulan = 12

    def __init__(self, merk, nama_model, harga, stok, harga_modal, power_output, jenis_koneksi):
        super().__init__(merk, nama_model, harga, stok, harga_modal)
        self.power_output = power_output
        self.jenis_koneksi = jenis_koneksi

    @classmethod
    def buat_dari_string(cls, data_string):
        merk, model, harga, stok, modal, power, koneksi = data_string.split(',')
        return cls(merk, model, int(harga), int(stok), int(modal), int(power), koneksi)

    @staticmethod
    def hitung_estimasi_cicilan(harga_barang, bulan):
        return harga_barang / bulan

    def terapkan_promo_bundling(self, persen):
        self._harga = int(self._harga * (1 - persen))
        print(f"[Promo] Harga {self.nama_model} turun {int(persen * 100)}% menjadi Rp{self._harga}.")

    def info_garansi(self):
        return f"Garansi resmi DAC {DAC.garansi_dac_bulan} bulan (lebih panjang dari garansi toko)"

    def tampilkan_info(self):
        super().tampilkan_info()
        print(f"   -> Tipe: DAC | Output: {self.power_output}mW | Koneksi: {self.jenis_koneksi}")


class Keranjang:
    def __init__(self):
        self.__daftar_produk = []

    @property
    def daftar_produk(self):
        return list(self.__daftar_produk)

    def tambah(self, produk):
        self.__daftar_produk.append(produk)

    def hitung_total(self):
        return sum(produk.harga for produk in self.__daftar_produk)

    def kosongkan(self):
        self.__daftar_produk.clear()

    def tampilkan_isi(self):
        if not self.__daftar_produk:
            print("   (keranjang kosong)")
        for nomor, produk in enumerate(self.__daftar_produk, start=1):
            print(f"   {nomor}. {produk.merk} {produk.nama_model} - Rp{produk.harga}")


class Toko:
    def __init__(self, nama):
        self.nama = nama
        self.__katalog = []

    def tambah_produk(self, produk):
        self.__katalog.append(produk)

    @property
    def jumlah_produk(self):
        return len(self.__katalog)

    def tampilkan_katalog(self):
        print(f"[KATALOG {self.nama.upper()}]")
        for produk in self.__katalog:
            produk.tampilkan_info()


class Pelanggan:
    total_pelanggan = 0
    diskon_member = 0.10
    level_member_default = "Reguler"

    def __init__(self, nama, perangkat_pemutar, saldo):
        self.nama = nama
        self.perangkat_pemutar = perangkat_pemutar
        self.__saldo = saldo
        self.keranjang = Keranjang()

        Pelanggan.total_pelanggan += 1

    @classmethod
    def ubah_diskon_member(cls, diskon_baru):
        cls.diskon_member = diskon_baru
        print(f"Diskon member untuk semua pelanggan diubah menjadi {cls.diskon_member * 100}%")

    @staticmethod
    def cek_kelayakan_beli(saldo, harga_barang):
        return saldo >= harga_barang

    @property
    def saldo(self):
        return self.__saldo

    @saldo.setter
    def saldo(self, nilai_baru):
        if nilai_baru < 0:
            print(f"[Validasi Gagal] Saldo {self.nama} tidak boleh negatif!")
        else:
            self.__saldo = nilai_baru
            print(f"[Validasi Sukses] Saldo {self.nama} berhasil diisi.")

    def konsultasi_daya(self, objek_iem):
        print(f"\n--- Sesi Konsultasi: {self.nama} ---")
        print(f"Perangkat Anda: {self.perangkat_pemutar}")
        print(f"Target IEM    : {objek_iem.merk} {objek_iem.nama_model} (Impedansi: {objek_iem.impedansi} Ohm)")

        if objek_iem.butuh_dac():
            print(">> HASIL: IEM ini BERAT. HP/Laptop Anda mungkin tidak kuat. Sangat disarankan membeli DAC tambahan!")
        else:
            print(">> HASIL: IEM ini RINGAN. Bisa langsung dicolok ke HP/Laptop Anda tanpa masalah daya.")

    def tambah_ke_keranjang(self, produk):
        if produk.stok <= 0:
            print(f"[Gagal] {produk.nama_model} sedang habis.")
        else:
            self.keranjang.tambah(produk)
            print(f"[Keranjang {self.nama}] {produk.nama_model} ditambahkan.")

    def checkout(self):
        total = self.keranjang.hitung_total()
        total_bayar = int(total * (1 - Pelanggan.diskon_member))
        print(f"\n--- Checkout: {self.nama} ---")
        self.keranjang.tampilkan_isi()
        print(f"   Total: Rp{total} | Setelah diskon member: Rp{total_bayar}")

        if Pelanggan.cek_kelayakan_beli(self.__saldo, total_bayar):
            for produk in self.keranjang.daftar_produk:
                produk.stok = produk.stok - 1
            self.__saldo -= total_bayar
            self.keranjang.kosongkan()
            print(f">> Pembayaran berhasil. Sisa saldo {self.nama}: Rp{self.__saldo}")
        else:
            print(f">> Pembayaran GAGAL. Saldo {self.nama} (Rp{self.__saldo}) tidak cukup.")


if __name__ == "__main__":
    print(f"=== Selamat Datang di {Produk.nama_toko} ===")

    iem1 = IEM("Kinera", "Wyvern Celest", 350000, 10, 280000, 32, "Dynamic Driver")
    iem2 = IEM("Sennheiser", "IE200", 2500000, 5, 2100000, 60, "Dynamic Driver")
    dac1 = DAC("Fiio", "BTR15", 1800000, 8, 1500000, 340, "Bluetooth")
    dac2 = DAC.buat_dari_string("Moondrop,DawnPro,800000,4,650000,120,USB-C")

    toko = Toko(Produk.nama_toko)
    for produk in (iem1, iem2, dac1, dac2):
        toko.tambah_produk(produk)

    pel1 = Pelanggan("Hammam", "Samsung Galaxy A13", 500000)
    pel2 = Pelanggan("Syamil", "Laptop Asus VivoBook", 3000000)

    print("\n[UJI AGREGASI: Toko memiliki Produk]")
    print(f"Jumlah produk di katalog: {toko.jumlah_produk}")
    toko.tampilkan_katalog()

    print("\n[UJI INHERITANCE & METHOD OVERRIDING]")
    print("Garansi IEM :", iem1.info_garansi())
    print("Garansi DAC :", dac1.info_garansi())
    print(f"isinstance(iem1, Produk) = {isinstance(iem1, Produk)}")
    print(f"isinstance(dac1, Produk) = {isinstance(dac1, Produk)}")
    print(f"isinstance(iem1, DAC)    = {isinstance(iem1, DAC)}")

    print("\n[UJI ASOSIASI: Pelanggan menggunakan IEM]")
    pel1.konsultasi_daya(iem1)
    pel2.konsultasi_daya(iem2)

    print("\n[UJI KOMPOSISI: Pelanggan memiliki Keranjang]")
    pel1.tambah_ke_keranjang(iem1)
    pel2.tambah_ke_keranjang(iem2)
    pel2.tambah_ke_keranjang(dac1)
    pel1.checkout()
    pel2.checkout()

    print("\n[UJI ATRIBUT PROTECTED DI SUBCLASS]")
    iem1.restock(5)
    dac1.terapkan_promo_bundling(0.10)

    print("\n[UJI ATRIBUT PRIVATE DI SUPERCLASS]")
    print(f"Margin {iem2.nama_model} via method superclass: Rp{iem2.hitung_margin()}")
    try:
        print(iem2.__harga_modal)
    except AttributeError:
        print("Akses langsung ke __harga_modal dari luar class -> AttributeError")

    print("\n[UJI CLASS METHOD & STATIC METHOD]")
    print(f"Total produk terdaftar: {Produk.total_produk}")
    print(f"Total pelanggan: {Pelanggan.total_pelanggan}")
    Pelanggan.ubah_diskon_member(0.15)
    print("Estimasi cicilan DAC Fiio BTR15 selama 6 bulan: Rp", DAC.hitung_estimasi_cicilan(dac1.harga, 6))
    print("Validasi nama merk 'Fiio':", Produk.validasi_nama_merk("Fiio"))

    print("\n[UJI GETTER, SETTER & VALIDASI]")
    print(">> Menguji input SALAH:")
    iem1.stok = -5
    iem1.stok = "Kosong"
    dac1.harga = 0
    pel1.saldo = -100000

    print("\n>> Menguji input BENAR:")
    iem1.stok = 15
    dac1.harga = 1700000
    pel1.saldo = 800000

    print("\n>> Cek data setelah diupdate via Getter:")
    print(f"Stok akhir {iem1.nama_model} = {iem1.stok}")
    print(f"Harga akhir {dac1.nama_model} = Rp{dac1.harga}")
    print(f"Saldo akhir {pel1.nama} = Rp{pel1.saldo}")

    print("\n[BUKTI AGREGASI: Produk tetap ada walau Toko dihapus]")
    del toko
    print(f"Toko dihapus, produk masih ada: {iem1.merk} {iem1.nama_model}")