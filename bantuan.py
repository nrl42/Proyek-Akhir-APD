import random
import string
import os

def clear():
    os.system('cls || clear')

def rupiah(angka):
    return "Rp" + format(angka, ",").replace(",", ".")

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