from database import baca_data, simpan_data, file_konser, file_akun, file_tiket
from bantuan import (rupiah, tanya_ya_tidak, tampilkan_rincian,
                     tampilkan_daftar_pesanan, tabel, clear, tekan_enter,
                     cetak_judul, sukses, gagal, peringatan, info, warna_status)
from beli_tiket import proses_pemesanan
from pesanan import cari_pesanan, pembayaran_terakhir
from pembayaran import batalkan_kadaluarsa, sisa_detik, format_sisa


def LihatInfoKonserDanKatalogTiket():
    clear()
    konser = baca_data(file_konser)
    tabel(["Keterangan", "Isi"], [
        ["Judul", konser["judul"]],
        ["Tanggal", konser["tanggal"]],
        ["Waktu", konser["waktu"]],
        ["Lokasi", konser["lokasi"]],
    ], judul="INFO KONSER")
    tabel(["Kategori", "Harga", "Sisa kuota"],
          [[k["jenis"], rupiah(k["harga"]), k["kuota"]] for k in konser["kategori"]],
          judul="KATALOG TIKET")
    tekan_enter()


def LihatDataPelanggan():
    clear()
    daftar_akun = baca_data(file_akun)
    pelanggan = [a for a in daftar_akun if a["role"].lower() == "user"]

    if len(pelanggan) == 0:
        cetak_judul("=====DATA PELANGGAN=====")
        peringatan("Belum ada data pelanggan")
        tekan_enter()
        return

    tabel(["No", "Username", "Nama", "No HP"],
          [[nomor, a["username"], a["nama"], a["no_hp"]]
           for nomor, a in enumerate(pelanggan, start=1)],
          judul="DATA PELANGGAN")
    tekan_enter()


def BuatPemesananPelanggan():
    clear()
    cetak_judul("=====BUAT PEMESANAN UNTUK PELANGGAN=====")
    username = input("Masukkan username pelanggan (0 untuk kembali): ").strip()
    if username == "0":
        return

    pelanggan = None
    for a in baca_data(file_akun):
        if a["username"] == username and a["role"].lower() == "user":
            pelanggan = a

    if pelanggan is None:
        gagal("Pelanggan tidak ditemukan")
        tekan_enter()
        return

    info("Pelanggan: " + pelanggan["nama"])
    tekan_enter()
    proses_pemesanan(pelanggan["username"])     


def PeriksaStatusPembayaran():
    clear()
    batalkan_kadaluarsa()
    cetak_judul("=====PERIKSA STATUS PEMBAYARAN=====")
    kode = input("Masukkan kode pemesanan (0 untuk kembali): ").strip().upper()
    if kode == "0":
        return

    pesanan = cari_pesanan(baca_data(file_tiket), kode)
    if pesanan is None:
        gagal("Pemesanan tidak ditemukan")
        tekan_enter()
        return

    bayar = pembayaran_terakhir(kode)
    baris = [
        ["Kode pesan", pesanan["kode_pesan"]],
        ["Pelanggan", pesanan["username"]],
        ["Tiket", f"{pesanan['kategori']} x {pesanan['jumlah']}"],
        ["Total bayar", rupiah(pesanan["total_bayar"])],
        ["Metode", bayar["metode"] if bayar is not None else "-"],
        ["Status pembayaran", warna_status(bayar["status"]) if bayar is not None else "Belum membayar"],
        ["Status pesanan", warna_status(pesanan["status"])],
        ["Status tiket", warna_status(pesanan["status_tiket"])],
        ["Kode unik", pesanan["kode_unik"] if pesanan["kode_unik"] else "-"],
    ]
    if pesanan["status"] == "Menunggu Pembayaran":
        baris.append(["Sisa waktu bayar", format_sisa(sisa_detik(pesanan))])
    tabel(["Keterangan", "Isi"], baris, judul="STATUS PEMBAYARAN")
    tekan_enter()


def LihatRincianHarga():
    clear()
    daftar_tiket = baca_data(file_tiket)
    if len(daftar_tiket) == 0:
        cetak_judul("=====RINCIAN HARGA & DISKON=====")
        peringatan("Belum ada data pemesanan")
        tekan_enter()
        return

    cetak_judul("=====RINCIAN HARGA & DISKON=====")
    tampilkan_daftar_pesanan(daftar_tiket)

    kode = input("Masukkan kode pemesanan (0 untuk kembali): ").strip().upper()
    if kode == "0":
        return

    pesanan = cari_pesanan(daftar_tiket, kode)
    if pesanan is None:
        gagal("kodePemesanan tidak ditemukan")
        tekan_enter()
        return
    tampilkan_rincian(pesanan)
    tekan_enter()


def KodeUnik():
    clear()
    cetak_judul("=====VALIDASI KODE UNIK TIKET=====")
    kode_unik = input("Masukkan kode unik (0 untuk kembali): ").strip().upper()
    if kode_unik == "0":
        return

    daftar_tiket = baca_data(file_tiket)
    ditemukan = None
    for t in daftar_tiket:
        if t["kode_unik"] == kode_unik and kode_unik != "":
            ditemukan = t

    if ditemukan is None:
        gagal("Tiket tidak valid")
    elif ditemukan["status_tiket"] != "Active":
        peringatan("Tiket sudah digunakan / tidak aktif (status: " + ditemukan["status_tiket"] + ")")
    else:
        ditemukan["status_tiket"] = "Used"
        simpan_data(file_tiket, daftar_tiket)
        sukses("Tiket valid, silakan masuk")
    tekan_enter()


def LihatDataTransaksi():
    clear()
    daftar_tiket = baca_data(file_tiket)
    if len(daftar_tiket) == 0:
        cetak_judul("=====DATA TRANSAKSI=====")
        peringatan("Belum ada transaksi")
    else:
        cetak_judul("=====DATA TRANSAKSI=====")
        tampilkan_daftar_pesanan(daftar_tiket)
    tekan_enter()


def Logout():
    if tanya_ya_tidak("Yakin ingin logout?"):
        sukses("Logout berhasil")
        return True
    peringatan("Logout dibatalkan")
    return False


def menu_petugas(akun):
    while True:
        batalkan_kadaluarsa()
        clear()
        cetak_judul("=== MENU PETUGAS ===")
        print("Selamat datang,", akun["nama"])
        print("1. Lihat info konser dan katalog tiket")
        print("2. Lihat data pelanggan")
        print("3. Bantu buat pemesanan pelanggan")
        print("4. Periksa status pembayaran")
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
            PeriksaStatusPembayaran()
        elif menu == "5":
            LihatRincianHarga()
        elif menu == "6":
            KodeUnik()
        elif menu == "7":
            LihatDataTransaksi()
        elif menu == "8":
            if Logout():
                break
            tekan_enter()
        else:
            gagal("Menu tidak valid")
            tekan_enter()
