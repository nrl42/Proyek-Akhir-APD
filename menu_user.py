from database import baca_data,simpan_data, file_tiket, file_pembatalan
from bantuan import rupiah, id_berikutnya, garis, waktu_sekarang
from beli_tiket import beli_tiket, bayar_pesanan

status_bisa_batal = ("menunggu pembayaran", "menunggu verifikasi", "lunas")

def status_pemesanan(akun):
    daftar_tiket = baca_data(file_tiket)

    print("\n=====STATUS PEMESANAN=====")
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

def bayar_pesanan_tertunda(akun):
    daftar_tiket = baca_data(file_tiket)
    print("\n=====BAYAR PESANAN=====")
    Menunggu = [t for t in daftar_tiket if t["username"] == akun["username"] and t["status"] == "menunggu pembayaran"]

    if len(menunggu) == 0:
        print("tidak ada pesanan yang menunggu pemabayaran")
        return

    for t in menunggu:
        print("tidak ada pesanan yang menunggu pembayaran")
        return

    kode = input("masukkan kode pesanan(0 untuk kembali) : ")
    if kode == "0":
        return

    for t in menunggu:
        if t["kode_pesanan"] == kode:
            bayar_pesanan(kode)
            return
    print("kode pesan tidak valid")

def cek_tiket():
    daftar_tiket = baca_data(file_tiket)

    print("\n=====CEK TIKET=====")
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
            print(f"{nomor}. {tiket['kode_pesan']} | {tiket['kategori']} x {tiket['jumlah']} | {rupiah(tiket['total_bayar'])} | kode unik: {tiket['kode_unik']}")

    if nomor == 0:
        print("Belum ada riwayat pembelian")

def ajukan_pembatalan():
    daftar_tiket = baca_data(file_tiket)
    daftar_batal = baca_data(file_pembatalan)

    print("\n=====AJUKAN PEMBATALAN TIKET=====")
    bisa_dibatalkan = []
    for tiket in daftar_tiket:
        if(tiket["username"] == akun["username"] and tiket["status"] in ("menunggu verifikasi","lunas") and tiket["status_tiket"] != "used"):
            bisa_dibatalkan.append(tiket)
            print(f"{tiket['kode_pesanan']} | {tiket['kategori']} × {tiket['jumlah']} |"
                f"{rupiah(tiket['total_bayar'])} | {tiket['status']}")
        
    if len(bisa_dibatalkan) == 0:
        print("Tidak ada pesanan yang dibatalkan")
        return

    kode = input("masukkan kode pesanan( input 0 untuk kembali): ").strip().upper()
    if kode == "0":
        return

    pesanan = None
    for tiket in bisa_dibatalkan:
        if tiket["kode_pesanan"] == kode:
            pesanan = tiket
    if pesanan is None:
        print("maaf kode tidak valid")
        return
        
    for b in daftar_batal:
        if b["kode_pesanan"] == kode and b["status"] == "menunggu":
            print("permintaan pembatalan untuk pesanan ini sudah diajukan")
            return

    alasan = ""
    while alasan == "":
        alasan = input("alasan pembatalan: ").strip()

    daftar_batal.append({
        "id": id_berikutnya(daftar_batal),
        "kode_pesan": kode,
        "username": akun["username"],
        "alasan": alasan,
        "status": "Menunggu"
    })
    simpan_data(file_tambahan, daftar_batal)
    print("permintaan pembatalan terikirim menunggu persetujuan admin")


def menu_user(akun):
    while True:
        print("\n=== MENU ===")
        print("Halo selamat datang,", akun["nama"])
        print("1.Beli Tiket")
        print("2.Status Pemesanan")
        print("3.Cek Tiket")
        print("4.Riwayat")
        print("5.ajukan_pembatalan")
        print("6.Logout")
        menu = input("Pilih menu: ")

        if menu == "1":
            beli_tiket(akun)
        elif menu == "2":
            status_pemesanan(akun)
        elif menu == "3":
            cek_tiket()
        elif menu == "4":
            riwayat_pembelian(akun)
        elif menu == "6":
            ajukan_pembatalan(akun)
        elif menu == "5":
            print("Berhasil logout.")
            break  
        else:
            print("Menu tidak valid")