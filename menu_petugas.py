from database import baca_data, simpan_data, file_konser, file_akun, file_tiket
from bantuan import (rupiah, garis, tanya_ya_tidak, tampilkan_rincian,
                     tampilkan_baris_pesanan, tabel, clear, tekan_enter)
from beli_tiket import proses_pemesanan
from pesanan import cari_pesanan, pembayaran_terakhir
from pembayaran import batalkan_kadaluarsa, sisa_detik, format_sisa


def LihatInfoKonserDanKatalogTiket():
    clear()
    konser = baca_data(file_konser)
    print("=====INFO KONSER=====")
    print("Judul   :", konser["judul"])
    print("Tanggal :", konser["tanggal"])
    print("Waktu   :", konser["waktu"])
    print("Lokasi  :", konser["lokasi"])
    print("\n=====KATALOG TIKET=====")
    for k in konser["kategori"]:
        print(f"- {k['jenis']}: {rupiah(k['harga'])} (sisa kuota: {k['kuota']})")
    tekan_enter()


def LihatDataPelanggan():
    clear()
    daftar_akun = baca_data(file_akun)
    pelanggan = [a for a in daftar_akun if a["role"].lower() == "user"]

    print("=====DATA PELANGGAN=====")
    if len(pelanggan) == 0:
        print("Belum ada data pelanggan")
        tekan_enter()
        return

    print(f"{'No':<4}{'Username':<15}{'Nama':<22}{'No HP':<15}")
    garis(56)
    for nomor, a in enumerate(pelanggan, start=1):
        print(f"{nomor:<4}{a['username']:<15}{a['nama']:<22}{a['no_hp']:<15}")
    tekan_enter()


def BuatPemesananPelanggan():
    clear()
    print("=====BUAT PEMESANAN UNTUK PELANGGAN=====")
    username = input("Masukkan username pelanggan (0 untuk kembali): ").strip()
    if username == "0":
        return

    pelanggan = None
    for a in baca_data(file_akun):
        if a["username"] == username and a["role"].lower() == "user":
            pelanggan = a

    if pelanggan is None:
        print("Pelanggan tidak ditemukan")
        tekan_enter()
        return

    print("Pelanggan:", pelanggan["nama"])
    tekan_enter()
    proses_pemesanan(pelanggan["username"])      # sudah punya jeda sendiri


def PeriksaStatusPembayaran():
    clear()
    batalkan_kadaluarsa()
    print("=====PERIKSA STATUS PEMBAYARAN=====")
    kode = input("Masukkan kode pemesanan (0 untuk kembali): ").strip().upper()
    if kode == "0":
        return

    pesanan = cari_pesanan(baca_data(file_tiket), kode)
    if pesanan is None:
        print("Pemesanan tidak ditemukan")
        tekan_enter()
        return

    bayar = pembayaran_terakhir(kode)
    baris = [
        ["Kode pesan", pesanan["kode_pesan"]],
        ["Pelanggan", pesanan["username"]],
        ["Tiket", f"{pesanan['kategori']} x {pesanan['jumlah']}"],
        ["Total bayar", rupiah(pesanan["total_bayar"])],
        ["Metode", bayar["metode"] if bayar is not None else "-"],
        ["Status pembayaran", bayar["status"] if bayar is not None else "Belum membayar"],
        ["Status pesanan", pesanan["status"]],
        ["Status tiket", pesanan["status_tiket"]],
        ["Kode unik", pesanan["kode_unik"] if pesanan["kode_unik"] else "-"],
    ]
    if pesanan["status"] == "Menunggu Pembayaran":
        baris.append(["Sisa waktu bayar", format_sisa(sisa_detik(pesanan))])
    tabel(["Keterangan", "Isi"], baris, judul="STATUS PEMBAYARAN")
    tekan_enter()


def LihatRincianHarga():
    clear()
    daftar_tiket = baca_data(file_tiket)
    print("=====RINCIAN HARGA & DISKON=====")
    if len(daftar_tiket) == 0:
        print("Belum ada data pemesanan")
        tekan_enter()
        return

    for nomor, t in enumerate(daftar_tiket, start=1):
        print(f"{nomor}. {t['kode_pesan']} | {t['username']} | {t['kategori']} x {t['jumlah']}")

    kode = input("Masukkan kode pemesanan (0 untuk kembali): ").strip().upper()
    if kode == "0":
        return

    pesanan = cari_pesanan(daftar_tiket, kode)
    if pesanan is None:
        print("kodePemesanan tidak ditemukan")
        tekan_enter()
        return
    tampilkan_rincian(pesanan)
    tekan_enter()


def KodeUnik():
    clear()
    print("=====VALIDASI KODE UNIK TIKET=====")
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
    tekan_enter()


def LihatDataTransaksi():
    clear()
    daftar_tiket = baca_data(file_tiket)
    print("=====DATA TRANSAKSI=====")
    if len(daftar_tiket) == 0:
        print("Belum ada transaksi")
    else:
        for t in daftar_tiket:
            tampilkan_baris_pesanan(t)
    tekan_enter()


def Logout():
    if tanya_ya_tidak("Yakin ingin logout?"):
        print("Logout berhasil")
        return True
    print("Logout dibatalkan")
    return False


def menu_petugas(akun):
    while True:
        batalkan_kadaluarsa()
        clear()
        print("=== MENU PETUGAS ===")
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
            print("Menu tidak valid")
            tekan_enter()