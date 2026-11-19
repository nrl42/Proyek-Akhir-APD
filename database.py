import json
import os

folder_data= "data"
file_akun = "data/akun_user.json"
file_tiket = "data/tiket.json"
file_konser = "data/konser.json"

def baca_data(nama_file):
    try:
        with open("nama_file/akun_user.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print("File tidak ditemukan:", "nama_file/akun_user.json")
        return []
    except json.JSONDecodeError:
        print("Isi file JSON rusak:", "nama_file/akun_user.json")
        return []

def simpan_data(nama_file,data):
    with open(nama_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)