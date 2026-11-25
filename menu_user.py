from database import baca_data, simpan_data, file_tiket, file_pembatalan
<<<<<<< HEAD
from bantuan import (rupiah, id_berikutnya, garis, waktu_sekarang, clear, tekan_enter, tabel)
=======
from bantuan import (rupiah, id_berikutnya, garis, waktu_sekarang, clear, tekan_enter, PrettyTable)
>>>>>>> bde7c84a32db483321e8b7c2ca094423c76ba97f
from beli_tiket import beli_tiket
from pembayaran import batalkan_kadaluarsa, sisa_detik, format_sisa



STATUS_BISA_BATAL = ("Menunggu Pembayaran", "Menunggu Verifikasi", "Lunas")


def status_pemesanan(akun):
    clear()
    batalkan_kadaluarsa()
    daftar_tiket = baca_data(file_tiket)

    print("=====STATUS PEMESANAN=====")
    ada = False
    for tiket in daftar_tiket:
        if tiket["username"] == akun["username"]:
            ada = True
            garis(30)
            print("Kode pesan :", tiket["kode_pesan"])
            print("Kategori   :", tiket["kategori"], "x", tiket["jumlah"])
            print("Harga awal :", rupiah(tiket["harga_awal"]))
            print("Diskon     :", rupiah(tiket["diskon"]))
            print("Total      :", rupiah(tiket["total_bayar"]))
            print("Status     :", tiket["status"])

    if not ada:
        print("Belum ada pemesanan.")
    tekan_enter()


def bayar_pesanan_tertunda(akun):
    clear()
    batalkan_kadaluarsa()
    daftar_tiket = baca_data(file_tiket)

    print("=====BAYAR PESANAN=====")
    menunggu = [t for t in daftar_tiket
                if t["username"] == akun["username"] and t["status"] == "Menunggu Pembayaran"]

    if len(menunggu) == 0:
        print("Tidak ada pesanan yang menunggu pembayaran.")
        tekan_enter()
        return

    for t in menunggu:
        print(f"{t['kode_pesan']} | {t['kategori']} x {t['jumlah']} | {rupiah(t['total_bayar'])} "
            f"| sisa waktu {format_sisa(sisa_detik(t))}")

    kode = input("Masukkan kode pesan (0 untuk kembali): ").strip().upper()
    if kode == "0":
        return

    for t in menunggu:
        if t["kode_pesan"] == kode:
            bayar_pesanan(kode)          
            return
    print("Kode pesan tidak valid.")
    tekan_enter()


def cek_tiket():
    clear()
    daftar_tiket = baca_data(file_tiket)

    print("=====CEK TIKET=====")
    while True:
        kode_unik = input("Masukkan kode unik (0 untuk kembali): ").strip().upper()

        if kode_unik == "0":
            return

        tiket_ketemu = None
        for tiket in daftar_tiket:
            if tiket["kode_unik"] == kode_unik and kode_unik != "":
                tiket_ketemu = tiket

        if tiket_ketemu is not None:
            print("\n=== STATUS TIKET ===")
            print("Kode pesan   :", tiket_ketemu["kode_pesan"])
            print("Kategori     :", tiket_ketemu["kategori"], "x", tiket_ketemu["jumlah"])
            print("Status       :", tiket_ketemu["status"])
            print("Status tiket :", tiket_ketemu["status_tiket"])
            tekan_enter()
            return

        print("Kode unik salah, coba lagi.")


def riwayat_pembelian(akun):
    clear()
    daftar_tiket = baca_data(file_tiket)

    print("=== RIWAYAT PEMBELIAN ===")
    nomor = 0
    for tiket in daftar_tiket:
        if tiket["username"] == akun["username"] and tiket["status"] == "Lunas":
            nomor = nomor + 1
            print(f"{nomor}. {tiket['kode_pesan']} | {tiket['kategori']} x {tiket['jumlah']} " f"| {rupiah(tiket['total_bayar'])} | kode unik: {tiket['kode_unik']}")

    if nomor == 0:
        print("Belum ada riwayat pembelian")
    tekan_enter()


def ajukan_pembatalan(akun):
    clear()
    daftar_tiket = baca_data(file_tiket)
    daftar_batal = baca_data(file_pembatalan)

    print("=====AJUKAN PEMBATALAN TIKET=====")
    bisa_dibatalkan = []
    for tiket in daftar_tiket:
        if (tiket["username"] == akun["username"]
                and tiket["status"] in STATUS_BISA_BATAL
                and tiket["status_tiket"] != "Used"):
            bisa_dibatalkan.append(tiket)
            print(f"{tiket['kode_pesan']} | {tiket['kategori']} x {tiket['jumlah']} | " f"{rupiah(tiket['total_bayar'])} | {tiket['status']}")

    if len(bisa_dibatalkan) == 0:
        print("Tidak ada pesanan yang bisa dibatalkan")
        tekan_enter()
        return

    kode = input("masukkan kode pesanan (input 0 untuk kembali): ").strip().upper()
    if kode == "0":
        return

    pesanan = None
    for tiket in bisa_dibatalkan:
        if tiket["kode_pesan"] == kode:
            pesanan = tiket
    if pesanan is None:
        print("maaf kode tidak valid")
        tekan_enter()
        return

    for b in daftar_batal:
        if b["kode_pesan"] == kode and b["status"] == "Menunggu":
            print("permintaan pembatalan untuk pesanan ini sudah diajukan")
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
    print("permintaan pembatalan terkirim, menunggu persetujuan admin")
    tekan_enter()


def menu_user(akun):
    while True:
        batalkan_kadaluarsa()
        clear()
        print("=== MENU ===")
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
            print("Berhasil logout.")
            break
        else:
            print("Menu tidak valid")
            tekan_enter()