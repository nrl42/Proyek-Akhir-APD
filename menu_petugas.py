from bantuan import (cetak_judul, cetak_menu, clear, gagal, info, peringatan,
                     rupiah, sukses, tabel, tampilkan_daftar_pesanan,
                     tampilkan_info_konser, tampilkan_katalog, tampilkan_rincian,
                     tanya_ya_tidak, tekan_enter, warna_status)
from beli_tiket import proses_pemesanan
from database import baca_data, file_akun, file_konser, file_tiket, simpan_data
from pembayaran import batalkan_kadaluarsa, format_sisa, sisa_detik
from pesanan import cari_pesanan, pembayaran_terakhir

OPSI_MENU = [
    "Lihat info konser dan katalog tiket",
    "Lihat data pelanggan",
    "Bantu buat pemesanan pelanggan",
    "Periksa status pembayaran",
    "Lihat data pemesanan",
    "Validasi kode unik tiket",
    "Lihat data transaksi",
    "Logout",
]


def LihatInfoKonserDanKatalogTiket():
    clear()
    konser = baca_data(file_konser)
    tampilkan_info_konser(konser)
    tampilkan_katalog(konser)
    tekan_enter()


def LihatDataPelanggan():
    clear()
    pelanggan = [a for a in baca_data(file_akun) if a["role"].lower() == "user"]

    if not pelanggan:
        cetak_judul("=====DATA PELANGGAN=====")
        peringatan("Belum ada data pelanggan")
    else:
        tabel(["No", "Username", "Nama", "No HP"],
              [[no, a["username"], a["nama"], a["no_hp"]]
               for no, a in enumerate(pelanggan, start=1)],
              judul="DATA PELANGGAN")
    tekan_enter()


def BuatPemesananPelanggan():
    clear()
    cetak_judul("=====BUAT PEMESANAN UNTUK PELANGGAN=====")
    username = input("Masukkan username pelanggan (Enter untuk kembali): ").strip()
    if username == "":
        return

    pelanggan = next((a for a in baca_data(file_akun)
                      if a["username"] == username and a["role"].lower() == "user"), None)
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
    kode = input("Masukkan kode pemesanan (Enter untuk kembali): ").strip().upper()
    if kode == "":
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
        ["Metode", bayar.get("metode", "-") if bayar else "-"],
        ["Status pembayaran", warna_status(bayar["status"]) if bayar else "Belum membayar"],
        ["Status pesanan", warna_status(pesanan["status"])],
        ["Status tiket", warna_status(pesanan["status_tiket"])],
        ["Kode unik", pesanan["kode_unik"] or "-"],
    ]
    if pesanan["status"] == "Menunggu Pembayaran":
        baris.append(["Sisa waktu bayar", format_sisa(sisa_detik(pesanan))])
    tabel(["Keterangan", "Isi"], baris, judul="STATUS PEMBAYARAN")
    tekan_enter()


def LihatDataPemesanan():
    while True:
        clear()
        daftar_tiket = baca_data(file_tiket)
        cetak_judul("=====LIHAT DATA PEMESANAN=====")
        if not daftar_tiket:
            peringatan("Belum ada data pemesanan")
            tekan_enter()
            return

        tampilkan_daftar_pesanan(daftar_tiket)
        kode = input("Masukkan kode pemesanan untuk rincian (Enter untuk kembali): ").strip().upper()
        if kode == "":
            return

        pesanan = cari_pesanan(daftar_tiket, kode)
        if pesanan is None:
            gagal("Kode pemesanan tidak ditemukan")
        else:
            tampilkan_rincian(pesanan)
        tekan_enter()


def KodeUnik():
    clear()
    cetak_judul("=====VALIDASI KODE UNIK TIKET=====")
    kode_unik = input("Masukkan kode unik (Enter untuk kembali): ").strip().upper()
    if kode_unik == "":
        return

    daftar_tiket = baca_data(file_tiket)
    tiket = next((t for t in daftar_tiket if t["kode_unik"] == kode_unik), None)

    if tiket is None:
        gagal("Tiket tidak valid")
    elif tiket["status_tiket"] != "Active":
        peringatan("Tiket sudah digunakan / tidak aktif (status: " + tiket["status_tiket"] + ")")
    else:
        tiket["status_tiket"] = "Used"
        simpan_data(file_tiket, daftar_tiket)
        sukses("Tiket valid, silakan masuk")
    tekan_enter()


def LihatDataTransaksi():
    clear()
    daftar_tiket = baca_data(file_tiket)
    cetak_judul("=====DATA TRANSAKSI=====")
    if not daftar_tiket:
        peringatan("Belum ada transaksi")
    else:
        tampilkan_daftar_pesanan(daftar_tiket)
    tekan_enter()


def Logout():
    if tanya_ya_tidak("Yakin ingin logout?"):
        sukses("Logout berhasil")
        return True
    peringatan("Logout dibatalkan")
    return False


def menu_petugas(akun):
    aksi = {
        "1": LihatInfoKonserDanKatalogTiket,
        "2": LihatDataPelanggan,
        "3": BuatPemesananPelanggan,
        "4": PeriksaStatusPembayaran,
        "5": LihatDataPemesanan,
        "6": KodeUnik,
        "7": LihatDataTransaksi,
    }
    while True:
        batalkan_kadaluarsa()
        clear()
        cetak_judul("=== MENU PETUGAS ===")
        print("Selamat datang,", akun["nama"])
        cetak_menu(OPSI_MENU)
        pilihan = input("Pilih menu: ").strip()

        if pilihan == "8":
            if Logout():
                break
            tekan_enter()
        elif pilihan in aksi:
            aksi[pilihan]()
        else:
            gagal("Menu tidak valid")
            tekan_enter()
