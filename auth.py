
import database as db

maks_percobaan = 3

def register_pelanggan():
    print("\nREGISTER PELANGGAN")
    nama = input("masukkan nama anda: ").strip()
    username = input("masukkan username anda: ").strip().lower()
    password = input("masukkan password anda: ").strip()

    if nama == "" or username == "" or password =="":
        print("semua data wajib diisi")
        return False

    if username == admin_username or db.cari_satu("data_akun_user", username=username):
        print("username sudah dipakai")
        return False

    akun = data_akun_user.tambah(username,password,nama,"pelanggan")

    data_pelanggan.tambah(akun["id"])
    print("selamat Register berhasil silahkan login")
    return True

def login():
    print("\n LOGIN")

    for percobaan in range(1, maks_percobaan + 1):
        username = input("username: ").strip().lower()
        password = input("password: ").strip()

        if username == admin_username and password == admin_password:
            print("selamat login berhasil di menu admin")
            return{"id": 0, "username": admin_username, "nama": "admin","role":"admin"}

        pengguna = data_akun_user.cari_login(username,password)
        if pengguna is not None:
            print(f"login berhasil{pengguna['nama']}!")
            return pengguna 
        
        sisa = maks_percobaan - percobaan
        if sisa > 0:
            print(f"username atau password salah, sisa percobaan : {sisa}")

    print("maaf percobaan login sudah habis kembali ke menu awal")
    return None

