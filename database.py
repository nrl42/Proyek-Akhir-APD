import json
import os
import copy

folder_data = "data"
file_akun = "data/akun_user.json"
file_tiket = "data/tiket.json"            
file_konser = "data/konser.json"          
file_diskon = "data/diskon.json"          
file_pembayaran = "data/pembayaran.json" 
file_pembatalan = "data/pembatalan.json"  

DATA_AWAL = {
    file_akun: [
        {"username": "laharah", "password": "laharah123", "nama": "nurdilpuj",
        "no_hp": "080000000001", "role": "Admin"},
        {"username": "petugas", "password": "petugas123", "nama": "rulaja",
        "no_hp": "080000000002", "role": "Petugas"},
        {"username": "nurul", "password": "nurul123", "nama": "nurul azizah",
        "no_hp": "081234329592", "role": "User"},
    ],
    file_tiket: [],
    file_konser: {
        "judul": "Konser Hindia",
        "tanggal": "20 Desember 2026",
        "waktu": "19.00 WITA",
        "lokasi": "Samarinda",
        "kategori": [
            {"nomor": 1, "jenis": "Reguler", "harga": 50000, "kuota": 100},
            {"nomor": 2, "jenis": "VIP", "harga": 100000, "kuota": 50},
            {"nomor": 3, "jenis": "VVIP", "harga": 150000, "kuota": 20},
        ],
    },
    file_diskon: [
        {"id": 1, "nama": "Diskon 2 tiket", "min_tiket": 2, "maks_tiket": 2, "persen": 5},
        {"id": 2, "nama": "Diskon 3-4 tiket", "min_tiket": 3, "maks_tiket": 4, "persen": 10},
    ],
    file_pembayaran: [],
    file_pembatalan: [],
}


def simpan_data(nama_file, data):
    with open(nama_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def siapkan_data():
    os.makedirs(folder_data, exist_ok=True)
    for nama_file, isi in DATA_AWAL.items():
        if not os.path.exists(nama_file):
            simpan_data(nama_file, isi)


def baca_data(nama_file):
    default = copy.deepcopy(DATA_AWAL.get(nama_file, []))
    try:
        with open(nama_file, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print("File tidak ditemukan:", nama_file)
        return default
    except json.JSONDecodeError:
        print("Isi file JSON rusak:", nama_file)
        return default
