import random
import string
import os
from datetime import datetime

from database import baca_data, file_diskon

MAKS_TIKET = 4


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
        print("Tidak boleh kosong!")


def tanya_ya_tidak(pesan):
    while True:
        jawab = input(pesan + " (y/n): ").strip().lower()
        if jawab == "y" or jawab == "ya":
            return True
        if jawab == "n" or jawab == "t" or jawab == "tidak":
            return False
        print("jawab dengan y atau n ")


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
    print("\n=====RINCIAN PEMESANAN=====")
    print("Kategori   :", pesanan["kategori"])
    print("Jumlah     :", pesanan["jumlah"])
    print("Harga awal :", rupiah(pesanan["harga_awal"]))
    print("Diskon     :", rupiah(pesanan["diskon"]))
    print("Total bayar:", rupiah(pesanan["total_bayar"]))


def tampilkan_struk(pesanan):
    print("\n===============")
    print("STRUK PEMESANAN")
    print("===============")
    print("Kode pesan :", pesanan["kode_pesan"])
    print("Kode unik  :", pesanan["kode_unik"] if pesanan["kode_unik"] else "-")
    print("Pemesan    :", pesanan["username"])
    print("Kategori   :", pesanan["kategori"])
    print("Jumlah     :", pesanan["jumlah"])
    print("Harga awal :", rupiah(pesanan["harga_awal"]))
    print("Diskon     :", rupiah(pesanan["diskon"]))
    print("Total bayar:", rupiah(pesanan["total_bayar"]))
    print("Status     :", pesanan["status"])
    print("===============")


def tampilkan_baris_pesanan(p):
    print(f"{p['kode_pesan']} | {p['username']} | {p['kategori']} x {p['jumlah']} | "
        f"{rupiah(p['total_bayar'])} | {p['status']}")



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
        print("\n=====" + judul + "=====")
    try:
        from prettytable import PrettyTable
        t = PrettyTable(list(kolom))
        t.align = "l"
        for b in baris:
            t.add_row([str(sel) for sel in b])
        print(t)
    except ImportError:
        lebar = [len(str(k)) for k in kolom]
        for b in baris:
            for i, sel in enumerate(b):
                lebar[i] = max(lebar[i], len(str(sel)))
        pemisah = "+" + "+".join("-" * (w + 2) for w in lebar) + "+"

        def cetak(isi):
            print("| " + " | ".join(str(s).ljust(w) for s, w in zip(isi, lebar)) + " |")

        print(pemisah)
        cetak(kolom)
        print(pemisah)
        for b in baris:
            cetak(b)
        print(pemisah)