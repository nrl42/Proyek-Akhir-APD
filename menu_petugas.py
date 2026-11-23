from database import (baca_data, simpan_data, file_konser, file_akun, file_tiket)
from bantuan import (rupiah, garis, input_wajib, tanya_ya_tidak, tampilkan_rincian,
                    tampilkan_baris_pesanan)
from beli_tiket import proses_pemesanan
from pesanan import cari_pesanan, pembayaran_terakhir
from bantuan import buat_kode_unik


def LihatInfoKonserDanKatalogTiket():
    konser = baca_data(file_konser)
    print("\n=====INFO KONSER=====")
    print("Judul   :", konser["judul"])
    print("Tanggal :", konser["tanggal"])
    print("Waktu   :", konser["waktu"])
    print("Lokasi  :", konser["lokasi"])
    print("\n=====KATALOG TIKET=====")
    for k in konser["kategori"]:
        print(f"- {k['jenis']}: {rupiah(k['harga'])} (sisa kuota: {k['kuota']})")


def LihatDataPelanggan():
    daftar_akun = baca_data(file_akun)
    pelanggan = [a for a in daftar_akun if a["role"].lower() == "user"]

    print("\n=====DATA PELANGGAN=====")
    if len(pelanggan) == 0:
        print("Belum ada data pelanggan")
        return

    print(f"{'No':<4}{'Username':<15}{'Nama':<22}{'No HP':<15}")
    garis(56)
    for nomor, a in enumerate(pelanggan, start=1):
        print(f"{nomor:<4}{a['username']:<15}{a['nama']:<22}{a['no_hp']:<15}")


def BuatPemesananPelanggan():
    print("\n=====BUAT PEMESANAN UNTUK PELANGGAN=====")
    username = input("Masukkan username pelanggan (0 untuk kembali): ").strip()
    if username == "0":
        return

    pelanggan = None
    for a in baca_data(file_akun):
        if a["username"] == username and a["role"].lower() == "user":
            pelanggan = a

    if pelanggan is None:
        print("Pelanggan tidak ditemukan")
        return

    print("Pelanggan:", pelanggan["nama"])
    proses_pemesanan(pelanggan["username"])


def PeriksaPembayaran():
    print("\n=====PERIKSA PEMBAYARAN=====")
    kode = input("Masukkan kode pemesanan (0 untuk kembali): ").strip().upper()
    if kode == "0":
        return

    daftar_tiket = baca_data(file_tiket)
    pesanan = cari_pesanan(daftar_tiket, kode)
    if pesanan is None:
        print("Pemesanan tidak ditemukan")
        return

    bayar = pembayaran_terakhir(kode)
    status_bayar = bayar["status"] if bayar is not None else "Menunggu Pembayaran"
    print("Status pembayaran :", status_bayar)
    print("Status pesanan    :", pesanan["status"])
    print("Status tiket      :", pesanan["status_tiket"])

    if status_bayar == "Terverifikasi":
        if pesanan["status_tiket"] in ("Active", "Used") and pesanan["kode_unik"] != "":
            print("Status tiket sudah diperbarui sebelumnya")
        else:
            pesanan["status_tiket"] = "Active"
            pesanan["kode_unik"] = buat_kode_unik(daftar_tiket)
            simpan_data(file_tiket, daftar_tiket)
            print("Pembayaran terverifikasi, status tiket Active, kode unik:", pesanan["kode_unik"])
    elif status_bayar == "Menunggu Verifikasi":
        print("Pembayaran belum terverifikasi (menunggu admin), status tiket tidak diubah")
    elif status_bayar == "Menunggu Pembayaran":
        print("Pelanggan belum membayar, status tiket tidak diubah")
    else:
        print("Pembayaran ditolak, status tiket tidak diubah")


def LihatRincianHarga():
    daftar_tiket = baca_data(file_tiket)
    print("\n=====RINCIAN HARGA & DISKON=====")
    if len(daftar_tiket) == 0:
        print("Belum ada data pemesanan")
        return

    for nomor, t in enumerate(daftar_tiket, start=1):
        print(f"{nomor}. {t['kode_pesan']} | {t['username']} | {t['kategori']} x {t['jumlah']}")

    kode = input("Masukkan kode pemesanan (0 untuk kembali): ").strip().upper()
    if kode == "0":
        return

    pesanan = cari_pesanan(daftar_tiket, kode)
    if pesanan is None:
        print("kodePemesanan tidak ditemukan")
        return
    tampilkan_rincian(pesanan)


def KodeUnik():
    print("\n=====VALIDASI KODE UNIK TIKET=====")
    kode_unik = input("Masukkan kode unik (0 untuk kembali): ").strip().upper()
    if kode_unik == "0":
        return

    daftar_tiket = baca_data(file_tiket)
    ditemukan = None
    for t in daftar_tiket:
        if t["kode_unik"] == kode_unik and kode_unik != "":
            ditemukan = t

    if ditemukan is None:
        print("Tiket tidak valid")
    elif ditemukan["status_tiket"] != "Active":
        print("Tiket sudah digunakan / tidak aktif (status:", ditemukan["status_tiket"] + ")")
    else:
        ditemukan["status_tiket"] = "Used"
        simpan_data(file_tiket, daftar_tiket)
        print("Tiket valid, silakan masuk")


def LihatDataTransaksi():
    daftar_tiket = baca_data(file_tiket)
    print("\n=====DATA TRANSAKSI=====")
    if len(daftar_tiket) == 0:
        print("Belum ada transaksi")
        return
    for t in daftar_tiket:
        tampilkan_baris_pesanan(t)


def Logout():
    if tanya_ya_tidak("Yakin ingin logout?"):
        print("Logout berhasil")
        return True
    print("Logout dibatalkan")
    return False


def menu_petugas(akun):
    while True:
        print("\n=== MENU PETUGAS ===")
        print("Selamat datang,", akun["nama"])
        print("1. Lihat info konser dan katalog tiket")
        print("2. Lihat data pelanggan")
        print("3. Bantu buat pemesanan pelanggan")
        print("4. Periksa status pembayaran dan ubah status tiket")
        print("5. Lihat rincian harga dan diskon")
        print("6. Validasi kode unik tiket")
        print("7. Lihat data transaksi")
        print("8. Logout")
        menu = input("Pilih menu: ").strip()

        if menu == "1":
            LihatInfoKonserDanKatalogTiket()
        elif menu == "2":
            LihatDataPelanggan()
        elif menu == "3":
            BuatPemesananPelanggan()
        elif menu == "4":
            PeriksaPembayaran()
        elif menu == "5":
            LihatRincianHarga()
        elif menu == "6":
            KodeUnik()
        elif menu == "7":
            LihatDataTransaksi()
        elif menu == "8":
            if Logout():
                break
        else:
            print("Menu tidak valid")
