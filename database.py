import json
import os

folder_data= "data"
file_akun = "data/akun_user.json"
file_tiket = "data/tiket.json"
file_konser = "data/konser.json"
file_diskon = "data/pembayaran.json"
file_pembayaran = "data/pembayaran.json"
file_pembatalan = "data/pembatalan.json"


def baca_data(nama_file, default=None):
    if default is None:
        if nama_file == file_konser:
            default = {}
        else:
            default = []

def baca_json(nama_file, default):
    try:
        with open(nama_file, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print("File tidak ditemukan:", nama_file)
        return default
    except json.JSONDecodeError:
        print("Isi file JSON rusak:", nama_file)
        return default

def simpan_data(nama_file, data):
    os.makedirs(os.path.dirname(nama_file), exist_ok=True)
    with open(nama_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
