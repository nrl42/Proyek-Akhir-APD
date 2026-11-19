from database import baca_data, file_tiket
from bantuan import rupiah
from beli_tiket import beli_tiket


def status_pemesanan(akun):
    daftar_tiket = baca_data(file_tiket)

    print("\n===== STATUS PEMESANAN =====")
    ada = False
    for tiket in daftar_tiket:
        if tiket["username"] == akun["username"]:
            ada = True
            print("-" * 30)
            print("Kode pesan :", tiket["kode_pesan"])
            print("Kategori   :", tiket["kategori"], "x", tiket["jumlah"])
            print("Harga awal :", rupiah(tiket["harga_awal"]))
            print("Diskon     :", rupiah(tiket["diskon"]))
            print("Total      :", rupiah(tiket["total_bayar"]))
            print("Status     :", tiket["status"])

    if not ada:
        print("Belum ada pemesanan.")


def cek_tiket():
    daftar_tiket = baca_data(file_tiket)

    print("\n=== CEK TIKET ===")
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
            print("Kode pesan :", tiket_ketemu["kode_pesan"])
            print("Kategori   :", tiket_ketemu["kategori"], "x", tiket_ketemu["jumlah"])
            print("Status     :", tiket_ketemu["status"])
            return

        print("Kode unik salah, coba lagi.")  


def riwayat_pembelian(akun):
    daftar_tiket = baca_data(file_tiket)

    print("\n=== RIWAYAT PEMBELIAN ===")
    nomor = 0
    for tiket in daftar_tiket:
        if tiket["username"] == akun["username"] and tiket["status"] == "Lunas":
            nomor = nomor + 1
            print(f"{nomor}. {tiket['kode_pesan']} | {tiket['kategori']} x {tiket['jumlah']} | {rupiah(tiket['total_bayar'])}")

    if nomor == 0:
        print("Belum ada riwayat pembelian.")


def menu_user(akun):
    while True:
        print("\n=== MENU ===")
        print("Halo,", akun["nama"])
        print("1.Beli Tiket")
        print("2.Status Pemesanan")
        print("3.Cek Tiket")
        print("4.Riwayat")
        print("5.Logout")
        menu = input("Pilih menu: ")

        if menu == "1":
            beli_tiket(akun)
        elif menu == "2":
            status_pemesanan(akun)
        elif menu == "3":
            cek_tiket()
        elif menu == "4":
            riwayat_pembelian(akun)
        elif menu == "5":
            print("Berhasil logout.")
            break  
        else:
            print("Menu tidak valid")