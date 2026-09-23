class IEM:
    nama_toko = "Audiophile HS Store"
    total_iem_terdaftar = 0
    batas_impedansi_berat = 50 

    def __init__(self, merk, nama_model, stok, harga, impedansi):
        self.merk = merk               
        self.nama_model = nama_model   
        self.impedansi = impedansi     
        self.__stok = stok
        self.__harga = harga           
        
        IEM.tambah_total_iem()

    @classmethod
    def tambah_total_iem(cls):
        cls.total_iem_terdaftar += 1

    @staticmethod
    def validasi_nama_merk(nama):
        return isinstance(nama, str) and len(nama) > 0

    @property
    def stok(self):
        return self.__stok

    def stok(self, nilai_baru):
        if not isinstance(nilai_baru, int):
            print(f"[Validasi Gagal] Stok {self.nama_model} harus berupa angka!")
        elif nilai_baru < 0:
            print(f"[Validasi Gagal] Stok {self.nama_model} tidak boleh negatif!")
        else:
            self.__stok = nilai_baru
            print(f"[Validasi Sukses] Stok {self.nama_model} berhasil diubah menjadi {self.__stok}.")

    def tampilkan_info(self):
        print(f"IEM: {self.merk} {self.nama_model} | {self.impedansi} Ohm | Rp{self.__harga} | Stok: {self.__stok}")


class DAC:
    kategori_barang = "Digital-to-Analog Converter (DAC)"
    total_dac_terdaftar = 0
    garansi_standar_bulan = 12

    def __init__(self, merk, nama_model, power_output, harga):
        self.merk = merk                 
        self.nama_model = nama_model     
        self.power_output = power_output 
        self.__harga = harga             
        
        DAC.total_dac_terdaftar += 1

    @classmethod
    def buat_dari_string(cls, data_string):
        merk, model, power, harga = data_string.split('-')
        return cls(merk, model, int(power), int(harga))

    @staticmethod
    def hitung_estimasi_cicilan(harga_barang, bulan):
        return harga_barang / bulan

    @property
    def harga(self):
        return self.__harga

    @harga.setter
    def harga(self, nilai_baru):
        if nilai_baru <= 0:
            print(f"[Validasi Gagal] Harga DAC {self.nama_model} tidak boleh 0 atau negatif!")
        else:
            self.__harga = nilai_baru

    def tampilkan_info(self):
        print(f"DAC: {self.merk} {self.nama_model} | Output: {self.power_output}mW | Harga: Rp{self.__harga}")


class Pelanggan:
    total_pelanggan = 0
    diskon_member = 0.10 # 10%
    level_member_default = "Reguler"

    def __init__(self, nama, perangkat_pemutar, saldo):
        self.nama = nama
        self.perangkat_pemutar = perangkat_pemutar
        self.__saldo = saldo # Private
        
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
        
        if objek_iem.impedansi > IEM.batas_impedansi_berat:
            print(">> HASIL: IEM ini BERAT. HP/Laptop Anda mungkin tidak kuat. Sangat disarankan membeli DAC tambahan!")
        else:
            print(">> HASIL: IEM ini RINGAN. Bisa langsung dicolok ke HP/Laptop Anda tanpa masalah daya.")

if __name__ == "__main__":
    print(f"=== Selamat Datang di {IEM.nama_toko} ===")

    iem1 = IEM("Kinera", "Wyvern Celest", 10, 350000, 32)
    iem2 = IEM("Sennheiser", "IE200", 5, 2500000, 60) 

    dac1 = DAC("Fiio", "BTR15", 340, 1800000)
    dac2 = DAC.buat_dari_string("Moondrop-DawnPro-120-800000") 

    pel1 = Pelanggan("Hammam", "Samsung Galaxy A13", 500000)
    pel2 = Pelanggan("Budi", "Laptop Asus VivoBook", 3000000)

    print("\n[KATALOG PRODUK]")
    iem1.tampilkan_info()
    iem2.tampilkan_info()
    dac1.tampilkan_info()
    dac2.tampilkan_info()

    # C. Uji Instance Method (Interaksi Antar Objek)
    pel1.konsultasi_daya(iem1) # Uji IEM ringan
    pel2.konsultasi_daya(iem2) # Uji IEM berat

    # D. Uji Class Method
    print("\n[UJI CLASS METHOD]")
    print(f"Total IEM terdaftar: {IEM.total_iem_terdaftar}")
    print(f"Total Pelanggan: {Pelanggan.total_pelanggan}")
    Pelanggan.ubah_diskon_member(0.15) # Mengubah nilai atribut kelas untuk semua objek

    # E. Uji Static Method
    print("\n[UJI STATIC METHOD]")
    # Static method tidak butuh objek, langsung panggil dari Class
    print("Cek kelayakan beli IEM2 (Rp2.500.000) dengan saldo Budi (Rp3.000.000):", 
          Pelanggan.cek_kelayakan_beli(pel2.saldo, 2500000))
    print("Estimasi cicilan DAC Fiio BTR15 selama 6 bulan: Rp", DAC.hitung_estimasi_cicilan(dac1.harga, 6))

    # F. Uji Getter, Setter, dan Validasi Data
    print("\n[UJI GETTER, SETTER & VALIDASI]")
    
    # Uji setter dengan data INVALID (Harus ditolak/print gagal)
    print(">> Menguji input SALAH:")
    iem1.stok = -5         # Stok negatif
    iem1.stok = "Kosong"   # Stok bukan integer
    pel1.saldo = -100000   # Saldo negatif

    # Uji setter dengan data VALID (Harus berhasil disimpan)
    print("\n>> Menguji input BENAR:")
    iem1.stok = 15         # Mengubah stok IEM
    pel1.saldo = 800000    # Menambah saldo pelanggan

    # Pembuktian Getter (Memanggil data yang sudah diperbarui)
    print("\n>> Cek data setelah diupdate via Getter:")
    print(f"Stok akhir {iem1.nama_model} = {iem1.stok}")
    print(f"Saldo akhir {pel1.nama} = Rp{pel1.saldo}")
