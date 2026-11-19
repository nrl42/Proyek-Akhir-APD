
import database as db
from auth import login, register_pelanggan
from bantuan import admin_password, admin_username, tampilkan_konser_hindia

from admin import menu_admin
from petugas import menu_petugas
from pelanggan import menu_pelanggan

def menu_awal():
    while True:
        print("\nTIKET KONSER HINDIA")
        print("1. login")
        print("2. Register")
        print("3. konser tersedia")
        print("4. logout")

        pilihan = input("pilih menu:").strip()

        if pilihan == "1":
            pengguna = login()

            if pengguna is not None:

                if pengguna["role"] == "admin":
                    menu_admin()
                    
                elif pengguna["role"] == "petugas":
                    menu_petugas(pengguna)

                elif pengguna["role"] == "pelanggan":
                    menu_pelanggan(pengguna)

        elif pilihan == "2":
            register()

        elif pilihan == "3":
            tampilkan_konser_hindia()

        elif pilihan == "4":
            print("terima kasih")
            break
        else:
            print("pilihan tidak valid")

def main():
    db.siapkan_database()
    menu_awal()

if __name__ == "__main__":
    main()
