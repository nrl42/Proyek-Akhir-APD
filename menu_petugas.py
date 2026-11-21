from database import baca_data, simpan_data, file_akun, file_konser, file_tiket, file_pembayaran
from bantuan import rupiah, tanya_ya_tidak
from beli_tiket import proses_pemesanan
from transaksi import (cari_pesanan, aktifkan_tiket, tampilkan_daftar_transaksi,
                        lihat_rincian_harga)


def lihat_info_konser_dan_katalog_tiket():
    konser = baca_data(file_konser)
    print("\n=====INFO KONSER=====")
    print("Judul   :", konser["judul"])
    print("Tanggal :", konser["tanggal"])
    print("Waktu   :", konser["waktu"])
    print("Lokasi  :", konser["lokasi"])
    print("\n=====KATALOG TIKET=====")
    for k in konser["kategori"]:
        print(f"- {k['jenis']}: {rupiah(k['harga'])} (sisa kuota: {k['kuota']})")


def lihat_data_pelanggan():
    daftar_akun = baca_data(file_akun)
    print("\n=====DATA PELANGGAN=====")
    nomor = 0
    for a in daftar_akun:
        if a["role"] == "User":
            nomor = nomor + 1
            print(f"{nomor}. {a['username']} | {a['nama']} | {a['no_hp']}")
    if nomor == 0:
        print("Belum ada data pelanggan.")


def buat_pemesanan_pelanggan():
    daftar_akun = baca_data(file_akun)
    print("\n=====BUAT PEMESANAN PELANGGAN=====")
    username = input("Masukkan username pelanggan: ").strip()

    pelanggan = None
    for a in daftar_akun:
        if a["username"] == username and a["role"] == "User":
            pelanggan = a

    if pelanggan is None:
        print("Pelanggan tidak ditemukan.")
        return

    print("Pelanggan:", pelanggan["nama"])
    proses_pemesanan(pelanggan["username"])


def periksa_pembayaran():
    daftar_tiket = baca_data(file_tiket)
    daftar_bayar = baca_data(file_pembayaran)
    print("\n=====PERIKSA PEMBAYARAN=====")
    kode = input("Masukkan kode pemesanan: ").strip().upper()

    pesanan = cari_pesanan(daftar_tiket, kode)
    if pesanan is None:
        print("Pemesanan tidak ditemukan.")
        return

    bayar = None
    for b in daftar_bayar:
        if b["kode_pesan"] == kode:
            bayar = b

    if bayar is None or bayar["status"] == "Menunggu Verifikasi":
        print("Pembayaran belum terverifikasi, status tiket tidak diubah.")
        return
    if bayar["status"] == "Ditolak" or bayar["status"] == "Dibatalkan":
        print("Pembayaran", bayar["status"].lower(), "- tiket tidak dapat diaktifkan.")
        return

    # status pembayaran = Terverifikasi
    if pesanan["status_tiket"] == "Active" or pesanan["status_tiket"] == "Used":
        print("Status tiket sudah diperbarui sebelumnya.")
        return

    pesanan["status"] = "Lunas"
    aktifkan_tiket(pesanan, daftar_tiket)
    simpan_data(file_tiket, daftar_tiket)
    print("Pembayaran terverifikasi, status tiket Active")
    print("Kode unik:", pesanan["kode_unik"])


def kode_unik():
    """Validasi tiket di pintu masuk: Active -> Used."""
    daftar_tiket = baca_data(file_tiket)
    print("\n=====CEK KODE UNIK (PINTU MASUK)=====")
    kode = input("Masukkan kode unik: ").strip().upper()

    tiket_ketemu = None
    for t in daftar_tiket:
        if t["kode_unik"] == kode and kode != "":
            tiket_ketemu = t

    if tiket_ketemu is None:
        print("Tiket tidak valid.")
        return
    if tiket_ketemu["status_tiket"] != "Active":
        print("Tiket sudah digunakan / tidak aktif. Status:", tiket_ketemu["status_tiket"])
        return

    tiket_ketemu["status_tiket"] = "Used"
    simpan_data(file_tiket, daftar_tiket)
    print("Tiket valid, silakan masuk.")
    print("Kategori:", tiket_ketemu["kategori"], "x", tiket_ketemu["jumlah"])


def lihat_data_transaksi():
    daftar_tiket = baca_data(file_tiket)
    if len(daftar_tiket) == 0:
        print("\nBelum ada transaksi.")
        return
    tampilkan_daftar_transaksi(daftar_tiket)


def menu_petugas(akun):
    while True:
        print("\n=== MENU PETUGAS ===")
        print("Selamat datang,", akun["nama"])
        print("1. Lihat info konser dan katalog tiket")
        print("2. Lihat data pelanggan")
        print("3. Bantu buat pemesanan tiket pelanggan")
        print("4. Periksa status pembayaran dan ubah status tiket")
        print("5. Lihat rincian harga dan diskon pembelian tiket")
        print("6. Cek kode unik tiket")
        print("7. Lihat data transaksi")
        print("8. Logout")
        menu = input("Pilih menu: ")

        if menu == "1":
            lihat_info_konser_dan_katalog_tiket()
        elif menu == "2":
            lihat_data_pelanggan()
        elif menu == "3":
            buat_pemesanan_pelanggan()
        elif menu == "4":
            periksa_pembayaran()
        elif menu == "5":
            lihat_rincian_harga()
        elif menu == "6":
            kode_unik()
        elif menu == "7":
            lihat_data_transaksi()
        elif menu == "8":
            if tanya_ya_tidak("Yakin ingin logout?"):
                print("Logout berhasil")
                break
            print("Logout dibatalkan")
        else:
            print("Menu tidak valid")
