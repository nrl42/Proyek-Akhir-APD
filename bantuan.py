import random
import string
import os
from datetime import datetime

from colorama import init, Fore, Style
from prettytable import PrettyTable

from database import baca_data, file_diskon

init(autoreset=True)

MAKS_TIKET = 4

WARNA_STATUS = {
    "Lunas": Fore.GREEN,
    "Terverifikasi": Fore.GREEN,
    "Active": Fore.GREEN,
    "Disetujui": Fore.GREEN,
    "Menunggu Pembayaran": Fore.YELLOW,
    "Menunggu Verifikasi": Fore.YELLOW,
    "Menunggu": Fore.YELLOW,
    "Used": Fore.CYAN,
    "Dibatalkan": Fore.RED,
    "Ditolak": Fore.RED,
}


def sukses(teks):
    print(Fore.GREEN + Style.BRIGHT + str(teks))


def gagal(teks):
    print(Fore.RED + Style.BRIGHT + str(teks))


def peringatan(teks):
    print(Fore.YELLOW + str(teks))


def info(teks):
    print(Fore.CYAN + str(teks))


def cetak_judul(teks):
    print(Fore.CYAN + Style.BRIGHT + str(teks))


def warna_status(status):
    """Kembalikan teks status yang sudah berwarna sesuai artinya."""
    return WARNA_STATUS.get(status, "") + str(status) + Style.RESET_ALL


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def garis(panjang=40, simbol="-"):
    print(simbol * panjang)


def waktu_sekarang():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def rupiah(angka):
    return "Rp" + format(angka, ",").replace(",", ".")


def input_angka(pesan):
    
    try:
        return int(input(pesan).strip())
    except ValueError:
        return -1


def input_angka_kosong(pesan):
    
    teks = input(pesan).strip()
    if teks == "":
        return None
    try:
        return int(teks)
    except ValueError:
        return -1


def input_wajib(pesan):
    
    while True:
        teks = input(pesan).strip()
        if teks != "":
            return teks
        gagal("Tidak boleh kosong!")


def tanya_ya_tidak(pesan):
    while True:
        jawab = input(pesan + " (y/n): ").strip().lower()
        if jawab == "y" or jawab == "ya":
            return True
        if jawab == "n" or jawab == "t" or jawab == "tidak":
            return False
        peringatan("jawab dengan y atau n ")


def id_berikutnya(daftar):
    terbesar = 0
    for d in daftar:
        if d["id"] > terbesar:
            terbesar = d["id"]
    return terbesar + 1


def buat_kode_pesanan(daftar_tiket):
    while True:
        kode = "PSN" + str(random.randint(1000, 9999))

        sudah_dipakai = False
        for tiket in daftar_tiket:
            if tiket["kode_pesan"] == kode:
                sudah_dipakai = True

        if not sudah_dipakai:
            return kode


def buat_kode_unik(daftar_tiket=None):
    
    if daftar_tiket is None:
        daftar_tiket = []
    kode_terpakai = {t.get("kode_unik") for t in daftar_tiket}  
    huruf_dan_angka = string.ascii_uppercase + string.digits
    while True:
        kode = "TKT-"
        for i in range(6):
            kode = kode + random.choice(huruf_dan_angka)
        if kode not in kode_terpakai:
            return kode


def persen_diskon(jumlah):
    persen = 0
    for d in baca_data(file_diskon):
        if d["min_tiket"] <= jumlah <= d["maks_tiket"]:
            persen = d["persen"]
    return persen


def hitung_diskon(jumlah, harga_awal):
    return harga_awal * persen_diskon(jumlah) // 100


def tampilkan_rincian(pesanan):
    tabel(["Keterangan", "Isi"], [
        ["Kategori", pesanan["kategori"]],
        ["Jumlah", pesanan["jumlah"]],
        ["Harga awal", rupiah(pesanan["harga_awal"])],
        ["Diskon", rupiah(pesanan["diskon"])],
        ["Total bayar", rupiah(pesanan["total_bayar"])],
    ], judul="RINCIAN PEMESANAN")


def tampilkan_struk(pesanan):
    tabel(["Keterangan", "Isi"], [
        ["Kode pesan", pesanan["kode_pesan"]],
        ["Kode unik", pesanan["kode_unik"] if pesanan["kode_unik"] else "-"],
        ["Pemesan", pesanan["username"]],
        ["Kategori", pesanan["kategori"]],
        ["Jumlah", pesanan["jumlah"]],
        ["Harga awal", rupiah(pesanan["harga_awal"])],
        ["Diskon", rupiah(pesanan["diskon"])],
        ["Total bayar", rupiah(pesanan["total_bayar"])],
        ["Status", warna_status(pesanan["status"])],
    ], judul="STRUK PEMESANAN")


def tampilkan_baris_pesanan(p):
    print(f"{p['kode_pesan']} | {p['username']} | {p['kategori']} x {p['jumlah']} | "
        f"{rupiah(p['total_bayar'])} | {warna_status(p['status'])}")


def tampilkan_daftar_pesanan(daftar):
    """Tabel ringkas untuk banyak pesanan sekaligus."""
    tabel(["Kode", "Username", "Kategori", "Jumlah", "Total", "Status"],
          [[p["kode_pesan"], p["username"], p["kategori"], p["jumlah"],
            rupiah(p["total_bayar"]), warna_status(p["status"])] for p in daftar])



def tekan_enter():
    input("\nTekan Enter untuk lanjut...")


def input_password(pesan="masukkan password anda: "):
    try:
        import pwinput
        return pwinput.pwinput(pesan, mask="*").strip()
    except ImportError:
        import getpass
        return getpass.getpass(pesan).strip()


def tabel(kolom, baris, judul=None):
    if judul:
        print()
        cetak_judul(f"====={judul}=====")
    t = PrettyTable([Fore.CYAN + Style.BRIGHT + str(k) + Style.RESET_ALL for k in kolom])
    t.align = "l"
    for b in baris:
        t.add_row([str(sel) for sel in b])
    print(t)