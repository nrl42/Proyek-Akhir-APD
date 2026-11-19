
from database import baca_data, simpan_data, file_akun



def login():
    daftar_akun= baca_data(file_akun)

    i = 0
    while i != 3:
        print("\n=====LOGIN=====")
        username = input("masukkan username anda: ")
        password = input("masukkan password anda: ")

        akun_cocok = None
        for akun in daftar_akun:
            if akun["username"] == username and akun["password"] == password:
                akun_cocok = akun

        if akun_cocok is not None:
            print("Selamat login berhasil")
            return akun_cocok

        print("maaf login gagal username atau password salah")
        i = i + 1

    print("gagal login 3 kali")
    return None

def register():
    daftar_akun = baca_data(file_akun)
    print("\n=====REGISTER=====")

    while True:
        username = input("username: ")

        sudah_terdaftar =  False
        for akun in["username"] == username:
            sudah_terdaftar = True

        if username == "":
            print("Username tidak boleh kosong!")
        elif sudah_terdaftar:           
            print("Username sudah dipakai!")
        else:                        
            break

    nama = input("masukkan nama anda :")
    password = input("masukkan password anda : ")
    no_hp = input("masukkan no HP anda :")

    akun_baru={
        "username": username,
        "password": password,
        "nama": nama,
        "no_hp": no_hp,
        "role": "User"
    }
    daftar_akun.append(akun_baru)
    simpan_data(file_akun, daftar_akun)
    print("Selamat Register berhasil silahkan login ke akun anda")
