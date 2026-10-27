from abc import ABC, abstractmethod
from getpass import getpass


def rupiah(angka):
    return "Rp" + f"{int(angka):,}".replace(",", ".")


def baca_teks(pesan):
    while True:
        nilai = input(pesan).strip()
        if nilai:
            return nilai
        print("Input tidak boleh kosong.")


def baca_angka(pesan, minimum=None):
    while True:
        try:
            nilai = int(input(pesan).strip())
        except ValueError:
            print("Masukkan angka bulat yang valid.")
            continue
        if minimum is not None and nilai < minimum:
            print(f"Nilai minimal adalah {minimum}.")
            continue
        return nilai


class Produk(ABC):
    nama_toko = "Audiophile HS Store"
    total_produk = 0
    garansi_standar_bulan = 6
    batas_promo = 0.10
    kategori = "Produk"
    spesifikasi_input = ()

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

    @classmethod
    def buat_dari_input(cls):
        merk = baca_teks("Merk              : ")
        nama_model = baca_teks("Nama model        : ")
        harga = baca_angka("Harga jual (Rp)   : ", 1)
        stok = baca_angka("Stok awal         : ", 0)
        harga_modal = baca_angka("Harga modal (Rp)  : ", 1)
        nilai_khusus = [pembaca(label) for label, pembaca in cls.spesifikasi_input]
        return cls(merk, nama_model, harga, stok, harga_modal, *nilai_khusus)

    @staticmethod
    def hitung_estimasi_cicilan(harga_barang, bulan):
        return harga_barang / bulan

    @property
    def harga(self):
        return self._harga

    @harga.setter
    def harga(self, nilai_baru):
        if not isinstance(nilai_baru, int) or nilai_baru <= 0:
            print(f"[Validasi Gagal] Harga {self.nama_model} harus angka lebih dari 0!")
        else:
            self._harga = nilai_baru
            print(f"[Berhasil] Harga {self.nama_model} diubah menjadi {rupiah(self._harga)}.")

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
            print(f"[Berhasil] Stok {self.nama_model} diubah menjadi {self._stok}.")

    @abstractmethod
    def info_spesifikasi(self):
        pass

    @abstractmethod
    def hitung_biaya_servis(self):
        pass

    def kurangi_stok(self, jumlah):
        self._stok -= jumlah

    def terapkan_promo(self, persen):
        if persen <= 0 or persen > self.batas_promo:
            print(f"[Gagal] Promo {self.nama_model} harus di atas 0% dan maksimal {int(self.batas_promo * 100)}%.")
            return
        self._harga = int(self._harga * (1 - persen))
        print(f"[Promo] Harga {self.nama_model} turun {round(persen * 100)}% menjadi {rupiah(self._harga)}.")

    def hitung_margin(self):
        return self._harga - self.__harga_modal

    def info_garansi(self):
        return f"Garansi toko {self.garansi_standar_bulan} bulan"

    def saran_daya(self):
        return "Produk ini tidak memerlukan konsultasi daya."

    def tampilkan_info(self):
        print(self)
        print(f"   Spesifikasi    : {self.info_spesifikasi()}")
        print(f"   Garansi        : {self.info_garansi()}")
        print(f"   Estimasi servis: {rupiah(self.hitung_biaya_servis())}")
        print(f"   Promo maksimal : {int(self.batas_promo * 100)}%")

    def __str__(self):
        return f"[{self.kategori}] {self.merk} {self.nama_model} | {rupiah(self._harga)} | Stok: {self._stok}"

    def __lt__(self, other):
        return self._harga < other._harga

    def __int__(self):
        return self._harga

    def __add__(self, other):
        return int(self) + int(other)

    def __radd__(self, other):
        return int(other) + int(self)


class IEM(Produk):
    kategori = "IEM"
    batas_impedansi_berat = 50
    batas_promo = 0.15
    spesifikasi_input = (
        ("Impedansi (Ohm)   : ", baca_angka),
        ("Jenis driver      : ", baca_teks),
    )

    def __init__(self, merk, nama_model, harga, stok, harga_modal, impedansi, jenis_driver):
        super().__init__(merk, nama_model, harga, stok, harga_modal)
        self.impedansi = impedansi
        self.jenis_driver = jenis_driver

    def butuh_dac(self):
        return self.impedansi > IEM.batas_impedansi_berat

    def info_spesifikasi(self):
        return f"Impedansi {self.impedansi} Ohm | Driver {self.jenis_driver}"

    def hitung_biaya_servis(self):
        return int(self._harga * 0.15)

    def info_garansi(self):
        return "Garansi toko 6 bulan (tidak termasuk kabel dan ear tips)"

    def saran_daya(self):
        if self.butuh_dac():
            return f"IEM ini BERAT ({self.impedansi} Ohm). HP/Laptop mungkin tidak kuat, disarankan membeli DAC."
        return f"IEM ini RINGAN ({self.impedansi} Ohm). Bisa langsung dicolok ke HP/Laptop."


class DAC(Produk):
    kategori = "DAC"
    garansi_dac_bulan = 12
    batas_promo = 0.20
    spesifikasi_input = (
        ("Output (mW)       : ", baca_angka),
        ("Jenis koneksi     : ", baca_teks),
    )

    def __init__(self, merk, nama_model, harga, stok, harga_modal, power_output, jenis_koneksi):
        super().__init__(merk, nama_model, harga, stok, harga_modal)
        self.power_output = power_output
        self.jenis_koneksi = jenis_koneksi

    @classmethod
    def buat_dari_string(cls, data_string):
        merk, model, harga, stok, modal, power, koneksi = data_string.split(',')
        return cls(merk, model, int(harga), int(stok), int(modal), int(power), koneksi)

    def info_spesifikasi(self):
        return f"Output {self.power_output}mW | Koneksi {self.jenis_koneksi}"

    def hitung_biaya_servis(self):
        return int(self._harga * 0.10) + 75000

    def info_garansi(self):
        return f"Garansi resmi DAC {DAC.garansi_dac_bulan} bulan"

    def saran_daya(self):
        if self.power_output >= 200:
            return f"DAC bertenaga ({self.power_output}mW), cocok untuk IEM berimpedansi tinggi."
        return f"DAC hemat daya ({self.power_output}mW), cocok untuk IEM sensitif berimpedansi rendah."


class Amplifier(Produk):
    kategori = "Amplifier"
    spesifikasi_input = (
        ("Daya (mW)         : ", baca_angka),
        ("Kelas amplifier   : ", baca_teks),
    )

    def __init__(self, merk, nama_model, harga, stok, harga_modal, daya_mw, kelas_amp):
        super().__init__(merk, nama_model, harga, stok, harga_modal)
        self.daya_mw = daya_mw
        self.kelas_amp = kelas_amp

    def info_spesifikasi(self):
        return f"Daya {self.daya_mw}mW | Kelas {self.kelas_amp}"

    def hitung_biaya_servis(self):
        return 100000 + self.daya_mw * 50

    def saran_daya(self):
        return f"Amplifier {self.daya_mw}mW cocok untuk headphone dan IEM berimpedansi tinggi."


class Keranjang:
    def __init__(self):
        self.__daftar_produk = []

    @property
    def daftar_produk(self):
        return list(self.__daftar_produk)

    def tambah(self, produk):
        self.__daftar_produk.append(produk)

    def jumlah_produk(self, produk):
        return self.__daftar_produk.count(produk)

    def hitung_total(self):
        return sum(self.__daftar_produk)

    def kosongkan(self):
        self.__daftar_produk.clear()

    def tampilkan_isi(self):
        if not self.__daftar_produk:
            print("   (keranjang kosong)")
        for nomor, produk in enumerate(self.__daftar_produk, start=1):
            print(f"   {nomor}. {produk.merk} {produk.nama_model} - {rupiah(produk.harga)}")

    def ringkasan(self):
        return f"Keranjang: {len(self)} item, total {rupiah(self.hitung_total())}"

    def __len__(self):
        return len(self.__daftar_produk)


class Toko:
    def __init__(self, nama):
        self.nama = nama
        self.__katalog = []

    @property
    def daftar_produk(self):
        return list(self.__katalog)

    def tambah_produk(self, produk):
        self.__katalog.append(produk)

    def ambil_produk(self, nomor):
        if 1 <= nomor <= len(self.__katalog):
            return self.__katalog[nomor - 1]
        return None

    def tampilkan_katalog(self, urut_harga=False):
        produk_tampil = sorted(self.__katalog) if urut_harga else self.__katalog
        print(f"\n=== KATALOG {self.nama.upper()} ===")
        for produk in produk_tampil:
            nomor = self.__katalog.index(produk) + 1
            print(f"{nomor:>2}. {produk}")
            print(f"    {produk.info_spesifikasi()}")

    def total_biaya_servis(self):
        return sum(produk.hitung_biaya_servis() for produk in self.__katalog)

    def ringkasan(self):
        return f"Toko {self.nama}: {len(self)} produk di katalog"

    def __len__(self):
        return len(self.__katalog)


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
        print(f"[Berhasil] Diskon member diubah menjadi {round(cls.diskon_member * 100)}%.")

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

    def isi_saldo(self, jumlah):
        if jumlah <= 0:
            print("[Validasi Gagal] Jumlah isi saldo harus lebih dari 0!")
            return
        self.saldo = self.saldo + jumlah
        print(f"[Berhasil] Saldo {self.nama} sekarang {rupiah(self.__saldo)}.")

    def konsultasi_daya(self, produk):
        print(f"\n--- Konsultasi Daya: {self.nama} ---")
        print(f"Perangkat Anda : {self.perangkat_pemutar}")
        print(f"Produk         : {produk.merk} {produk.nama_model}")
        print(f">> {produk.saran_daya()}")

    def tambah_ke_keranjang(self, produk):
        if produk.stok - self.keranjang.jumlah_produk(produk) <= 0:
            print(f"[Gagal] Stok {produk.nama_model} tidak mencukupi.")
            return
        self.keranjang.tambah(produk)
        print(f"[Berhasil] {produk.nama_model} ditambahkan ke keranjang {self.nama}.")

    def checkout(self):
        if len(self.keranjang) == 0:
            print("[Gagal] Keranjang masih kosong.")
            return
        total = self.keranjang.hitung_total()
        potongan = int(total * Pelanggan.diskon_member)
        total_bayar = total - potongan
        print(f"\n--- Struk Checkout: {self.nama} ---")
        self.keranjang.tampilkan_isi()
        print(f"   Subtotal      : {rupiah(total)}")
        print(f"   Diskon member : {rupiah(potongan)} ({round(Pelanggan.diskon_member * 100)}%)")
        print(f"   Total bayar   : {rupiah(total_bayar)}")

        if not Pelanggan.cek_kelayakan_beli(self.__saldo, total_bayar):
            kurang = total_bayar - self.__saldo
            print(f">> Pembayaran GAGAL. Saldo {rupiah(self.__saldo)} kurang {rupiah(kurang)}.")
            return

        for produk in self.keranjang.daftar_produk:
            produk.kurangi_stok(1)
        self.__saldo -= total_bayar
        self.keranjang.kosongkan()
        print(f">> Pembayaran berhasil. Sisa saldo: {rupiah(self.__saldo)}")

    def ringkasan(self):
        return f"Pelanggan {self.nama}: saldo {rupiah(self.__saldo)}, {len(self.keranjang)} item di keranjang"


JENIS_PRODUK = {"1": IEM, "2": DAC, "3": Amplifier}


def cetak_ringkasan(*daftar_objek):
    for objek in daftar_objek:
        print(objek.ringkasan())


def buat_toko_awal():
    toko = Toko(Produk.nama_toko)
    toko.tambah_produk(IEM("Kinera", "Wyvern Celest", 350000, 10, 280000, 32, "Dynamic Driver"))
    toko.tambah_produk(IEM("Sennheiser", "IE200", 2500000, 5, 2100000, 60, "Dynamic Driver"))
    toko.tambah_produk(DAC("Fiio", "BTR15", 1800000, 8, 1500000, 340, "Bluetooth"))
    toko.tambah_produk(DAC.buat_dari_string("Moondrop,DawnPro,800000,4,650000,120,USB-C"))
    toko.tambah_produk(Amplifier("Topping", "L30II", 1600000, 3, 1300000, 1000, "Class AB"))
    return toko


def pilih_produk(toko):
    nomor = baca_angka("Masukkan nomor produk: ")
    produk = toko.ambil_produk(nomor)
    if produk is None:
        print("[Gagal] Nomor produk tidak ditemukan.")
    return produk


def menu_katalog(toko, pelanggan):
    jawaban = baca_teks("Urutkan dari termurah? (y/n): ").lower()
    toko.tampilkan_katalog(urut_harga=(jawaban == "y"))


def menu_detail(toko, pelanggan):
    toko.tampilkan_katalog()
    produk = pilih_produk(toko)
    if produk is None:
        return
    print()
    produk.tampilkan_info()
    for bulan in (6, 12):
        cicilan = Produk.hitung_estimasi_cicilan(produk.harga, bulan)
        print(f"   Cicilan {bulan:>2} bulan: {rupiah(cicilan)} per bulan")


def menu_konsultasi(toko, pelanggan):
    toko.tampilkan_katalog()
    produk = pilih_produk(toko)
    if produk is not None:
        pelanggan.konsultasi_daya(produk)


def menu_tambah_keranjang(toko, pelanggan):
    toko.tampilkan_katalog()
    produk = pilih_produk(toko)
    if produk is not None:
        pelanggan.tambah_ke_keranjang(produk)


def menu_lihat_keranjang(toko, pelanggan):
    print(f"\n=== KERANJANG {pelanggan.nama.upper()} ===")
    pelanggan.keranjang.tampilkan_isi()
    print(f"   Total sebelum diskon: {rupiah(pelanggan.keranjang.hitung_total())}")


def menu_checkout(toko, pelanggan):
    menu_lihat_keranjang(toko, pelanggan)
    if len(pelanggan.keranjang) == 0:
        return
    jawaban = baca_teks("Lanjutkan pembayaran? (y/n): ").lower()
    if jawaban == "y":
        pelanggan.checkout()
    else:
        print("Checkout dibatalkan.")


def menu_isi_saldo(toko, pelanggan):
    print(f"Saldo saat ini: {rupiah(pelanggan.saldo)}")
    pelanggan.isi_saldo(baca_angka("Jumlah isi saldo (Rp): "))


def menu_ringkasan(toko, pelanggan):
    print("\n=== RINGKASAN ===")
    cetak_ringkasan(toko, pelanggan.keranjang, pelanggan)


PIN_ADMIN = "123456"
MAKS_PERCOBAAN_PIN = 3


def menu_arsitektur(toko):
    print("\n=== INFO ARSITEKTUR PROGRAM ===")
    print("Produk adalah abstract class. Mencoba membuat objek Produk langsung:")
    try:
        Produk("Merk", "Model", 1000, 1, 500)
    except TypeError as galat:
        print(f"TypeError: {galat}")
    print("\nAbstract method pada Produk:", ", ".join(sorted(Produk.__abstractmethods__)))
    print("Subclass dan status implementasinya:")
    for kelas in Produk.__subclasses__():
        kurang = sorted(kelas.__abstractmethods__)
        status = "lengkap, bisa dibuat objeknya" if not kurang else "belum lengkap: " + ", ".join(kurang)
        print(f"   {kelas.__name__:<10}: {status}")


def admin_lihat_katalog(toko):
    toko.tampilkan_katalog()


def admin_tambah_produk(toko):
    print("\nJenis produk yang bisa ditambahkan:")
    for nomor, kelas in JENIS_PRODUK.items():
        print(f"   {nomor}. {kelas.kategori}")
    kelas = JENIS_PRODUK.get(baca_teks("Pilih jenis: "))
    if kelas is None:
        print("[Gagal] Jenis produk tidak tersedia.")
        return
    produk = kelas.buat_dari_input()
    toko.tambah_produk(produk)
    print(f"[Berhasil] {produk.merk} {produk.nama_model} masuk katalog. Total produk di toko: {len(toko)}.")


def admin_ubah_stok(toko):
    toko.tampilkan_katalog()
    produk = pilih_produk(toko)
    if produk is not None:
        produk.stok = baca_angka("Stok baru: ")


def admin_ubah_harga(toko):
    toko.tampilkan_katalog()
    produk = pilih_produk(toko)
    if produk is not None:
        produk.harga = baca_angka("Harga baru (Rp): ")


def admin_promo(toko):
    toko.tampilkan_katalog()
    produk = pilih_produk(toko)
    if produk is not None:
        produk.terapkan_promo(baca_angka("Persentase promo (%): ") / 100)


def admin_diskon_member(toko):
    persen = baca_angka("Diskon member baru (0-50 %): ")
    if 0 <= persen <= 50:
        Pelanggan.ubah_diskon_member(persen / 100)
    else:
        print("[Gagal] Diskon harus antara 0 sampai 50 persen.")


def admin_laporan(toko):
    print("\n=== LAPORAN MARGIN & BIAYA SERVIS ===")
    for produk in toko.daftar_produk:
        print(f"{produk.kategori:<10}{produk.nama_model:<15} margin {rupiah(produk.hitung_margin()):<12} servis {rupiah(produk.hitung_biaya_servis())}")
    print(f"Total estimasi biaya servis seluruh produk: {rupiah(toko.total_biaya_servis())}")
    print(f"Jumlah produk terdaftar (counter class)   : {Produk.total_produk}")


MENU_PELANGGAN = {
    "1": ("Lihat katalog", menu_katalog),
    "2": ("Detail produk", menu_detail),
    "3": ("Konsultasi daya", menu_konsultasi),
    "4": ("Tambah ke keranjang", menu_tambah_keranjang),
    "5": ("Lihat keranjang", menu_lihat_keranjang),
    "6": ("Checkout", menu_checkout),
    "7": ("Isi saldo", menu_isi_saldo),
    "8": ("Ringkasan toko & akun", menu_ringkasan),
}

MENU_ADMIN = {
    "1": ("Lihat katalog", admin_lihat_katalog),
    "2": ("Tambah produk baru", admin_tambah_produk),
    "3": ("Ubah stok produk", admin_ubah_stok),
    "4": ("Ubah harga produk", admin_ubah_harga),
    "5": ("Terapkan promo", admin_promo),
    "6": ("Ubah diskon member", admin_diskon_member),
    "7": ("Laporan margin & servis", admin_laporan),
    "8": ("Info arsitektur program", menu_arsitektur),
}


def jalankan_menu(judul, daftar_menu, label_keluar, *argumen):
    while True:
        print("\n" + "=" * 40)
        print(f"{judul:^40}")
        print("=" * 40)
        for nomor, (label, _) in daftar_menu.items():
            print(f"{nomor:>2}. {label}")
        print(f" 0. {label_keluar}")
        pilihan = input("Pilih menu: ").strip()
        if pilihan == "0":
            return
        aksi = daftar_menu.get(pilihan)
        if aksi is None:
            print("Menu tidak tersedia, silakan pilih lagi.")
            continue
        aksi[1](*argumen)


def verifikasi_admin():
    for percobaan in range(1, MAKS_PERCOBAAN_PIN + 1):
        if getpass("PIN admin: ") == PIN_ADMIN:
            return True
        print(f"[Gagal] PIN salah ({percobaan}/{MAKS_PERCOBAAN_PIN}).")
    return False


def sesi_pelanggan(toko):
    print("\n--- Login Pelanggan ---")
    nama = baca_teks("Nama Anda                     : ")
    perangkat = baca_teks("Perangkat pemutar (HP/Laptop): ")
    saldo = baca_angka("Saldo awal (Rp)               : ", 0)

    pelanggan = Pelanggan(nama, perangkat, saldo)
    print(f"\nHalo, {pelanggan.nama}! Selamat berbelanja.")
    jalankan_menu(f"MENU PELANGGAN - {pelanggan.nama.upper()}", MENU_PELANGGAN, "Logout", toko, pelanggan)
    print(f"Sampai jumpa, {pelanggan.nama}!")


def sesi_admin(toko):
    print("\n--- Login Admin ---")
    if not verifikasi_admin():
        print("Akses admin ditolak.")
        return
    print("Login admin berhasil.")
    jalankan_menu("MENU ADMIN", MENU_ADMIN, "Logout", toko)
    print("Admin telah logout.")


MENU_PERAN = {
    "1": ("Masuk sebagai Pelanggan", sesi_pelanggan),
    "2": ("Masuk sebagai Admin", sesi_admin),
}


def main():
    print(f"=== Selamat Datang di {Produk.nama_toko} ===")
    toko = buat_toko_awal()
    jalankan_menu(Produk.nama_toko.upper(), MENU_PERAN, "Keluar program", toko)
    print("Terima kasih, program selesai.")


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nProgram dihentikan.")