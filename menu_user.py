from database import baca_data, simpan_data, file_tiket, file_pembatalan
from bantuan import (rupiah, id_berikutnya, waktu_sekarang, clear, tekan_enter, tabel,
cetak_judul, sukses, gagal, peringatan, info, warna_status)
from beli_tiket import beli_tiket
from pembayaran import batalkan_kadaluarsa, sisa_detik, format_sisa, bayar_pesanan


STATUS_BISA_BATAL = ("Menunggu Pembayaran", "Menunggu Verifikasi", "Lunas")


def status_pemesanan(akun):
    clear()
    batalkan_kadaluarsa()
    daftar_tiket = baca_data(file_tiket)

    milik_user = [t for t in daftar_tiket if t["username"] == akun["username"]]
    if len(milik_user) == 0:
        cetak_judul("=====STATUS PEMESANAN=====")
        peringatan("Belum ada pemesanan.")
    else:
        tabel(["Kode", "Kategori", "Jumlah", "Harga awal", "Diskon", "Total", "Status"],
        [[t["kode_pesan"], t["kategori"], t["jumlah"], rupiah(t["harga_awal"]),
                rupiah(t["diskon"]), rupiah(t["total_bayar"]), warna_status(t["status"])]
                for t in milik_user],
                judul="STATUS PEMESANAN")
    tekan_enter()


def bayar_pesanan_tertunda(akun):
    clear()
    batalkan_kadaluarsa()
    daftar_tiket = baca_data(file_tiket)

    menunggu = [t for t in daftar_tiket
                if t["username"] == akun["username"] and t["status"] == "Menunggu Pembayaran"]

    if len(menunggu) == 0:
        cetak_judul("=====BAYAR PESANAN=====")
        peringatan("Tidak ada pesanan yang menunggu pembayaran.")
        tekan_enter()
        return

    tabel(["Kode", "Kategori", "Jumlah", "Total", "Sisa waktu"],
    [[t["kode_pesan"], t["kategori"], t["jumlah"], rupiah(t["total_bayar"]),
    format_sisa(sisa_detik(t))] for t in menunggu],
    judul="BAYAR PESANAN")

    kode = input("Masukkan kode pesan (0 untuk kembali): ").strip().upper()
    if kode == "0":
        return

    for t in menunggu:
        if t["kode_pesan"] == kode:
            bayar_pesanan(kode)
            return
    gagal("Kode pesan tidak valid.")
    tekan_enter()


def cek_tiket():
    clear()
    daftar_tiket = baca_data(file_tiket)

    cetak_judul("=====CEK TIKET=====")
    while True:
        kode_unik = input("Masukkan kode unik (0 untuk kembali): ").strip().upper()

        if kode_unik == "0":
            return

        tiket_ketemu = None
        for tiket in daftar_tiket:
            if tiket["kode_unik"] == kode_unik and kode_unik != "":
                tiket_ketemu = tiket

        if tiket_ketemu is not None:
            tabel(["Keterangan", "Isi"], [
                ["Kode pesan", tiket_ketemu["kode_pesan"]],
                ["Kategori", f"{tiket_ketemu['kategori']} x {tiket_ketemu['jumlah']}"],
                ["Status", warna_status(tiket_ketemu["status"])],
                ["Status tiket", warna_status(tiket_ketemu["status_tiket"])],
            ], judul="STATUS TIKET")
            tekan_enter()
            return

        gagal("Kode unik salah, coba lagi.")


def riwayat_pembelian(akun):
    clear()
    daftar_tiket = baca_data(file_tiket)

    lunas = [t for t in daftar_tiket
    if t["username"] == akun["username"] and t["status"] == "Lunas"]

    if len(lunas) == 0:
        cetak_judul("=== RIWAYAT PEMBELIAN ===")
        peringatan("Belum ada riwayat pembelian")
    else:
        tabel(["No", "Kode pesan", "Kategori", "Jumlah", "Total", "Kode unik"],
        [[no, t["kode_pesan"], t["kategori"], t["jumlah"],
        rupiah(t["total_bayar"]), t["kode_unik"]]
        for no, t in enumerate(lunas, start=1)],
        judul="RIWAYAT PEMBELIAN")
    tekan_enter()


def ajukan_pembatalan(akun):
    clear()
    daftar_tiket = baca_data(file_tiket)
    daftar_batal = baca_data(file_pembatalan)

    bisa_dibatalkan = [t for t in daftar_tiket
    if t["username"] == akun["username"]
    and t["status"] in STATUS_BISA_BATAL
    and t["status_tiket"] != "Used"]

    if len(bisa_dibatalkan) == 0:
        cetak_judul("=====AJUKAN PEMBATALAN TIKET=====")
        peringatan("Tidak ada pesanan yang bisa dibatalkan")
        tekan_enter()
        return

    tabel(["Kode", "Kategori", "Jumlah", "Total", "Status"],
    [[t["kode_pesan"], t["kategori"], t["jumlah"], rupiah(t["total_bayar"]),
    warna_status(t["status"])] for t in bisa_dibatalkan],
    judul="AJUKAN PEMBATALAN TIKET")

    kode = input("masukkan kode pesanan (input 0 untuk kembali): ").strip().upper()
    if kode == "0":
        return

    pesanan = None
    for tiket in bisa_dibatalkan:
        if tiket["kode_pesan"] == kode:
            pesanan = tiket
    if pesanan is None:
        gagal("maaf kode tidak valid")
        tekan_enter()
        return

    for b in daftar_batal:
        if b["kode_pesan"] == kode and b["status"] == "Menunggu":
            peringatan("permintaan pembatalan untuk pesanan ini sudah diajukan")
            tekan_enter()
            return

    alasan = ""
    while alasan == "":
        alasan = input("alasan pembatalan: ").strip()

    daftar_batal.append({
        "id": id_berikutnya(daftar_batal),
        "kode_pesan": kode,
        "username": akun["username"],
        "alasan": alasan,
        "waktu": waktu_sekarang(),
        "status": "Menunggu"
    })
    simpan_data(file_pembatalan, daftar_batal)
    sukses("permintaan pembatalan terkirim, menunggu persetujuan admin")
    tekan_enter()


def menu_user(akun):
    while True:
        batalkan_kadaluarsa()
        clear()
        cetak_judul("=== MENU ===")
        print("Halo selamat datang,", akun["nama"])
        print("1. Beli Tiket")
        print("2. Bayar Pesanan")
        print("3. Status Pemesanan")
        print("4. Cek Tiket")
        print("5. Riwayat")
        print("6. Ajukan Pembatalan")
        print("7. Logout")
        menu = input("Pilih menu: ").strip()

        if menu == "1":
            beli_tiket(akun)
        elif menu == "2":
            bayar_pesanan_tertunda(akun)
        elif menu == "3":
            status_pemesanan(akun)
        elif menu == "4":
            cek_tiket()
        elif menu == "5":
            riwayat_pembelian(akun)
        elif menu == "6":
            ajukan_pembatalan(akun)
        elif menu == "7":
            info("Berhasil logout.")
            break
        else:
            gagal("Menu tidak valid")
            tekan_enter()
