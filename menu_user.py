from bantuan import (cetak_judul, cetak_menu, clear, gagal, id_berikutnya, info,
                     input_wajib, peringatan, rupiah, sukses, tabel, tekan_enter,
                     waktu_sekarang, warna_status)
from beli_tiket import beli_tiket
from database import baca_data, file_pembatalan, file_tiket, simpan_data
from pembayaran import bayar_pesanan, batalkan_kadaluarsa, format_sisa, sisa_detik
from pesanan import STATUS_AKTIF

OPSI_MENU = ["Beli Tiket", "Bayar Pesanan", "Status Pemesanan", "Cek Tiket",
             "Riwayat", "Ajukan Pembatalan", "Logout"]


def status_pemesanan(akun):
    clear()
    batalkan_kadaluarsa()
    milik_user = [t for t in baca_data(file_tiket) if t["username"] == akun["username"]]

    if not milik_user:
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
    menunggu = [t for t in baca_data(file_tiket)
                if t["username"] == akun["username"] and t["status"] == "Menunggu Pembayaran"]

    if not menunggu:
        cetak_judul("=====BAYAR PESANAN=====")
        peringatan("Tidak ada pesanan yang menunggu pembayaran.")
        tekan_enter()
        return

    tabel(["Kode", "Kategori", "Jumlah", "Total", "Sisa waktu"],
          [[t["kode_pesan"], t["kategori"], t["jumlah"], rupiah(t["total_bayar"]),
            format_sisa(sisa_detik(t))] for t in menunggu],
          judul="BAYAR PESANAN")

    kode = input("Masukkan kode pesan (Enter untuk kembali): ").strip().upper()
    if kode == "":
        return

    if any(t["kode_pesan"] == kode for t in menunggu):
        bayar_pesanan(kode)
        return
    gagal("Kode pesan tidak valid.")
    tekan_enter()


def cek_tiket(akun):
    """Cek status tiket milik sendiri berdasarkan kode unik."""
    clear()
    daftar_tiket = baca_data(file_tiket)
    milik_user = [t for t in daftar_tiket if t["username"] == akun["username"]]

    cetak_judul("=====CEK TIKET=====")
    while True:
        kode_unik = input("Masukkan kode unik (Enter untuk kembali): ").strip().upper()
        if kode_unik == "":
            return

        tiket = next((t for t in milik_user
                      if t["kode_unik"] and t["kode_unik"] == kode_unik), None)
        if tiket is not None:
            tabel(["Keterangan", "Isi"], [
                ["Kode pesan", tiket["kode_pesan"]],
                ["Kategori", f"{tiket['kategori']} x {tiket['jumlah']}"],
                ["Status", warna_status(tiket["status"])],
                ["Status tiket", warna_status(tiket["status_tiket"])],
            ], judul="STATUS TIKET")
            tekan_enter()
            return

        gagal("Kode unik salah, coba lagi.")


def riwayat_pembelian(akun):
    clear()
    lunas = [t for t in baca_data(file_tiket)
             if t["username"] == akun["username"] and t["status"] == "Lunas"]

    if not lunas:
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
                       and t["status"] in STATUS_AKTIF
                       and t["status_tiket"] != "Used"]

    if not bisa_dibatalkan:
        cetak_judul("=====AJUKAN PEMBATALAN TIKET=====")
        peringatan("Tidak ada pesanan yang bisa dibatalkan")
        tekan_enter()
        return

    tabel(["Kode", "Kategori", "Jumlah", "Total", "Status"],
          [[t["kode_pesan"], t["kategori"], t["jumlah"], rupiah(t["total_bayar"]),
            warna_status(t["status"])] for t in bisa_dibatalkan],
          judul="AJUKAN PEMBATALAN TIKET")

    kode = input("masukkan kode pesanan (Enter untuk kembali): ").strip().upper()
    if kode == "":
        return

    if not any(t["kode_pesan"] == kode for t in bisa_dibatalkan):
        gagal("maaf kode tidak valid")
        tekan_enter()
        return

    if any(b["kode_pesan"] == kode and b["status"] == "Menunggu" for b in daftar_batal):
        peringatan("permintaan pembatalan untuk pesanan ini sudah diajukan")
        tekan_enter()
        return

    alasan = input_wajib("alasan pembatalan: ")
    daftar_batal.append({
        "id": id_berikutnya(daftar_batal),
        "kode_pesan": kode,
        "username": akun["username"],
        "alasan": alasan,
        "waktu": waktu_sekarang(),
        "status": "Menunggu",
    })
    simpan_data(file_pembatalan, daftar_batal)
    sukses("permintaan pembatalan terkirim, menunggu persetujuan admin")
    tekan_enter()


def menu_user(akun):
    aksi = {
        "1": lambda: beli_tiket(akun),
        "2": lambda: bayar_pesanan_tertunda(akun),
        "3": lambda: status_pemesanan(akun),
        "4": lambda: cek_tiket(akun),
        "5": lambda: riwayat_pembelian(akun),
        "6": lambda: ajukan_pembatalan(akun),
    }
    while True:
        batalkan_kadaluarsa()
        clear()
        cetak_judul("=== MENU ===")
        print("Halo selamat datang,", akun["nama"])
        cetak_menu(OPSI_MENU)
        pilihan = input("Pilih menu: ").strip()

        if pilihan == "7":
            info("Berhasil logout.")
            break
        if pilihan in aksi:
            aksi[pilihan]()
        else:
            gagal("Menu tidak valid")
            tekan_enter()
