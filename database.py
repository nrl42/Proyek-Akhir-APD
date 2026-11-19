import json
import os

folder_data= "data"
lokasi_file = "data/akun_user.json"

def siapkan_database():
    os.makedirs("data", exist_ok = True)

    if not os.path.exists(lokasi_file):
        data_awal = {
            "admin":[],
            "petugas":[],
            "pelanggan": []
        }

        simpan_database(data_awal)

def baca_database():
    with open(lokasi_file, "r") as file:
        return json.load(file)

def simpan_database():
    with open(lokasi_file, "w") as file:
        json.dump(data,file,indent=4)

def cari_login(username, password):
    data= baca_database()

    for role in data:
        for akun in data[role]:
            if akun["username"] == username and akun ["password"] == password:
                return akun

    return None

def cari_username(username):
    data = baca_database()

    for role in data:
        for akun in data[role]:
            if akun["username"] == username:
                return akun

    return None

def tambah_pelanggan (nama,username,password):
    data = baca_database()

    semua_id = []

    for role in data:
        for akun in data[role]:
            semua_id.append(akun["id"])

    id_baru = max(semua_id, default=0) + 1

    akun_baru = {
        "id" : id_baru,
        "nama": nama,
        "username": username,
        "password": password,
        "role": pelanggan
    }

    data["pelanggan"].append(akun_baru)

    simpan_database(data)

    return akun_baru