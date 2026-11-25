from bantuan import (cetak_judul, clear, gagal, input_no_hp, input_password,
                     input_wajib, sukses)
from database import baca_data, file_akun, simpan_data

MAKS_PERCOBAAN = 3


def login():
    akun_per_username = {a["username"]: a for a in baca_data(file_akun)}

    for percobaan in range(1, MAKS_PERCOBAAN + 1):
        clear()
        cetak_judul("=====LOGIN=====")
        username = input("masukkan username anda: ").strip()
        password = input_password("masukkan password anda: ")

        akun = akun_per_username.get(username)
        if akun is not None and akun["password"] == password:
            sukses("Selamat login berhasil")
            return akun

        gagal(f"maaf login gagal username atau password salah "
              f"(percobaan {percobaan}/{MAKS_PERCOBAAN})")
        if percobaan < MAKS_PERCOBAAN:
            input("Tekan Enter untuk coba lagi...")

    gagal(f"gagal login {MAKS_PERCOBAAN} kali")
    return None


def register():
    clear()
    daftar_akun = baca_data(file_akun)
    username_terdaftar = {a["username"] for a in daftar_akun}
    cetak_judul("=====REGISTER=====")

    while True:
        username = input_wajib("username: ")
        if username not in username_terdaftar:
            break
        gagal("Username sudah dipakai!")

    nama = input_wajib("masukkan nama anda : ")

    while True:
        password = input_password("masukkan password anda : ")
        ulang = input_password("ulangi password anda : ")
        if password == "":
            gagal("Password tidak boleh kosong!")
        elif password != ulang:
            gagal("Password tidak sama, coba lagi.")
        else:
            break

    no_hp = input_no_hp("masukkan no HP anda : ")

    daftar_akun.append({
        "username": username,
        "password": password,
        "nama": nama,
        "no_hp": no_hp,
        "role": "User",
    })
    simpan_data(file_akun, daftar_akun)
    sukses("Selamat Register berhasil silahkan login ke akun anda")
