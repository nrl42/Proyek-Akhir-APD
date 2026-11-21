import random
import string
import os

def clear():
    os.system('cls || clear')

def rupiah(angka):
    return "Rp" + format(angka, ",").replace(",", ".")

def input_angka(pesan):
    try:
        return int(input(pesan).strip())
    except ValueError:
        return -1

def input_angka_kosong(pesan):
    teks = input(pesan.strip())
    if teks == "":
        return None
    try:
        return int(teks)
    except ValueError:
        return -1

def tanya_ya_tidak(pesan):
    while True:
        jawab = input(pesan + "(y/n):").strip().lower()
        if jawab == "y" or jawab =="ya":
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

def buat_kode_unik():
    huruf_dan_angka = string.ascii_uppercase + string.digits
    kode = "TKT-"
    for i in range(6):
        kode = kode + random.choice(huruf_dan_angka)
    return kode