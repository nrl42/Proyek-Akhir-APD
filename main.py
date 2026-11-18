
import database as db
from admin import menu_admin
from bantuan import admin_password, admin_username, tampilkan_konser_hindia
from pelanggan import menu_pelanggan, register_pelanggan 
from petugas import menu_petugas


def menu_awal():
    while True:
        print("\nTIKET KONSER HINDIA")
        print("1. login")
        print("2. Register")
        print("3. konser tersedia")
        print("4. logout")
        pilihan = input("pilih menu:").strip()

        if pilihan == "1":
            login()
        elif pilihan == "2":
            register()
        elif pilihan == "3":
            tampilkan_konser_hindia()
        elif pilihan == "4":
            print("terima kasih")
            break
        else:
            print("pilihan tidak valid")

def login():
    print("\n LOGIN TIKET KONSER HINDIA")
    username = input("username: ").strip()
    password = input("password: "). strip()

    if username == admin_username and password == admin_password:
        menu_admin()
        return

    pengguna = db.cari_satu("pengguna", username=username, password=db.hash_password(password))

    if pengguna is None:
        print("username atau password salah")
    elif pengguna["role"] == "petugas":
        menu_petugas(pengguna) 
    else:
        menu_pelanggan(pengguna)

def main():
    db.siapkan_database()
    menu_awal()

if__name__ == "__main__":
    main()

