from database import buat_database, isi_data_awal
from utils import tampilkan_info_konser
from auth import register, login, login_admin
from pelanggan import menu_pelanggan
from petugas import menu_petugas
from admin import menu_admin

def main():
    buat_database()
    isi_data_awal()

    while True:
        print("\n==============================")
        print("TIKET KONSER HINDIA ")
        print("==============================")
        tampilkan_info_konser()

        while True:
        print("\n--- MENU ---")
        print("1. Login")
        print("2. Register")
        print("3. Konser Tersedia")
        print("4. Logout")
        pilih = input("Pilih menu: ")