from database import baca_data, simpan_data, file_akun
from bantuan import clear, input_password


def login():
    daftar_akun = baca_data(file_akun)
    akun_per_username = {akun["username"]: akun for akun in daftar_akun}

    percobaan = 0
    while percobaan < 3:
        clear()
        print("=====LOGIN=====")
        username = input("masukkan username anda: ").strip()
        password = input_password("masukkan password anda: ")

        akun = akun_per_username.get(username)
        if akun is not None and akun["password"] == password:
            print("Selamat login berhasil")
            return akun

        percobaan += 1
        print(f"maaf login gagal username atau password salah (percobaan {percobaan}/3)")
        if percobaan < 3:
            input("Tekan Enter untuk coba lagi...")

    print("gagal login 3 kali")
    return None


def register():
    clear()
    daftar_akun = baca_data(file_akun)
    username_terdaftar = {akun["username"] for akun in daftar_akun}
    print("=====REGISTER=====")

    while True:
        username = input("username: ").strip()
        if username == "":
            print("Username tidak boleh kosong!")
        elif username in username_terdaftar:
            print("Username sudah dipakai!")
        else:
            break

    nama = input("masukkan nama anda : ").strip()

    while True:
        password = input_password("masukkan password anda : ")
        ulang = input_password("ulangi password anda : ")
        if password == "":
            print("Password tidak boleh kosong!")
        elif password != ulang:
            print("Password tidak sama, coba lagi.")
        else:
            break

    while True:
        no_hp = input("masukkan no HP anda : ").strip()
        try:
            int(no_hp)                      
            if not 10 <= len(no_hp) <= 13:
                raise ValueError("panjang no HP salah")
            break
        except ValueError:
            print("No HP harus berupa 10-13 digit angka!")

    if nama == "":
        print("Nama tidak boleh kosong, register dibatalkan.")
        return

    daftar_akun.append({
        "username": username,
        "password": password,
        "nama": nama,
        "no_hp": no_hp,
        "role": "User"
    })
    simpan_data(file_akun, daftar_akun)
    print("Selamat Register berhasil silahkan login ke akun anda")
