import getpass
import os
import random
import string
from datetime import datetime

from colorama import Fore, Style, init
from prettytable import PrettyTable

from database import baca_data, file_diskon

try:
    import pwinput
except ImportError:
    pwinput = None

init(autoreset=True)

MAKS_TIKET = 4
FORMAT_WAKTU = "%Y-%m-%d %H:%M:%S"

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
    return WARNA_STATUS.get(status, "") + str(status) + Style.RESET_ALL


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def tekan_enter():
    input("\nTekan Enter untuk lanjut...")


def cetak_menu(daftar_opsi):
    for nomor, teks in enumerate(daftar_opsi, start=1):
        print(f"{nomor}. {teks}")


def tabel(kolom, baris, judul=None):
    if judul:
        print()
        cetak_judul(f"====={judul}=====")
    t = PrettyTable([Fore.CYAN + Style.BRIGHT + str(k) + Style.RESET_ALL for k in kolom])
    t.align = "l"
    for b in baris:
        t.add_row([str(sel) for sel in b])
    print(t)


def waktu_sekarang():
    return datetime.now().strftime(FORMAT_WAKTU)


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


def input_no_hp(pesan="No HP : ", boleh_kosong=False):
    while True:
        no_hp = input(pesan).strip()
        if boleh_kosong and no_hp == "":
            return ""
        if no_hp.isascii() and no_hp.isdigit() and 11 <= len(no_hp) <= 13 \
                and no_hp.startswith("08"):
            return no_hp
        gagal("No HP harus 11-13 digit angka dan diawali 08!")


def input_password(pesan="masukkan password anda: "):
    if pwinput is not None:
        return pwinput.pwinput(pesan, mask="*").strip()
    return getpass.getpass(pesan).strip()


def tanya_ya_tidak(pesan):
    while True:
        jawab = input(pesan + " (y/n): ").strip().lower()
        if jawab in ("y", "ya"):
            return True
        if jawab in ("n", "t", "tidak"):
            return False
        peringatan("jawab dengan y atau n")


def id_berikutnya(daftar):
    return max((d["id"] for d in daftar), default=0) + 1


def buat_kode_pesanan(daftar_tiket):
    terpakai = {t["kode_pesan"] for t in daftar_tiket}
    while True:
        kode = f"PSN{random.randint(1000, 9999)}"
        if kode not in terpakai:
            return kode


def buat_kode_unik(daftar_tiket=()):
    terpakai = {t.get("kode_unik") for t in daftar_tiket}
    karakter = string.ascii_uppercase + string.digits
    while True:
        kode = "TKT-" + "".join(random.choices(karakter, k=6))
        if kode not in terpakai:
            return kode


def persen_diskon(jumlah):
    persen = 0
    for d in baca_data(file_diskon):
        if d["min_tiket"] <= jumlah <= d["maks_tiket"]:
            persen = d["persen"]
    return persen


def hitung_diskon(jumlah, harga_awal):
    return harga_awal * persen_diskon(jumlah) // 100


def tampilkan_info_konser(konser):
    tabel(["Keterangan", "Isi"], [
        ["Judul", konser["judul"]],
        ["Tanggal", konser["tanggal"]],
        ["Waktu", konser["waktu"]],
        ["Lokasi", konser["lokasi"]],
    ], judul="INFO KONSER")


def tampilkan_katalog(konser):
    tabel(["No", "Kategori", "Harga", "Sisa kuota"],
          [[k["nomor"], k["jenis"], rupiah(k["harga"]), k["kuota"]]
           for k in konser["kategori"]],
          judul="KATALOG TIKET")


def tampilkan_rincian(pesanan):
    harga_awal = pesanan["harga_awal"]
    persen = pesanan["diskon"] * 100 // harga_awal if harga_awal else 0
    tabel(["Keterangan", "Isi"], [
        ["Kategori", pesanan["kategori"]],
        ["Jumlah", pesanan["jumlah"]],
        ["Harga awal", rupiah(harga_awal)],
        ["Diskon", f"{rupiah(pesanan['diskon'])} ({persen}%)"],
        ["Total bayar", rupiah(pesanan["total_bayar"])],
    ], judul="RINCIAN PEMESANAN")


def tampilkan_struk(pesanan):
    tabel(["Keterangan", "Isi"], [
        ["Kode pesan", pesanan["kode_pesan"]],
        ["Kode unik", pesanan["kode_unik"] or "-"],
        ["Pemesan", pesanan["username"]],
        ["Kategori", pesanan["kategori"]],
        ["Jumlah", pesanan["jumlah"]],
        ["Harga awal", rupiah(pesanan["harga_awal"])],
        ["Diskon", rupiah(pesanan["diskon"])],
        ["Total bayar", rupiah(pesanan["total_bayar"])],
        ["Status", warna_status(pesanan["status"])],
    ], judul="STRUK PEMESANAN")


def tampilkan_daftar_pesanan(daftar):
    tabel(["Kode", "Username", "Kategori", "Jumlah", "Total", "Status"],
          [[p["kode_pesan"], p["username"], p["kategori"], p["jumlah"],
            rupiah(p["total_bayar"]), warna_status(p["status"])] for p in daftar])
