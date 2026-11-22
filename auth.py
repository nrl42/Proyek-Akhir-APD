
from database import baca_data, simpan_data, file_akun



def login():
    daftar_akun= baca_data(file_akun)

    i = 0
    while i != 3:
        print("\n=====LOGIN=====")
        username = input("masukkan username anda: ").strip()
        password = input("masukkan password anda: ").strip()

        akun_cocok = None
        for akun in daftar_akun:
            if akun["username"] == username and akun["password"] == password:
                akun_cocok = akun

        if akun_cocok is not None:
            print("Selamat login berhasil")
            return akun_cocok

        i = i + 1
        print("maaf login gagal username atau password salah")

    print("gagal login 3 kali")
    return None

def register():
    daftar_akun = baca_data(file_akun)
    print("\n=====REGISTER=====")

    while True:
        username = input("username: ").strip()

        sudah_terdaftar =  False
        for akun in daftar_akun:
            if akun["username"] == username:
                sudah_terdaftar = True

        if username == "":
            print("Username tidak boleh kosong!")
        elif sudah_terdaftar:           
            print("Username sudah dipakai!")
        else:                        
            break

    nama = input("masukkan nama anda :").strip()
    password = input("masukkan password anda : ").strip()
    no_hp = input("masukkan no HP anda :").strip()

    if nama == "" or password == "" or no_hp == "":
        print(" mohon maaf Data tidak lengkap")
        return
        
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
