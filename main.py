from database import baca_data, file_konser, siapkan_data
from bantuan import rupiah
from auth import login, register
from menu_user import menu_user
from menu_petugas import menu_petugas
from menu_admin import menu_admin

def tampilkan_kategori_tiket():
    konser = baca_data(file_konser)
    print("\n kategori tiket yang tersedia:")
    for k in konser["kategori"]:
        print(f"- {k['jenis']}: {rupiah(k['harga'])} (sisa kuota: {k['kuota']})")


def masuk_sesuai_role(akun):
    role = akun["role"].lower()
    if role == "admin":
        menu_admin(akun)
    elif role == "petugas":
        menu_petugas(akun)
    else:
        menu_user(akun)


def main():
    siapkan_data()   

    while True:

        print("\n=====MENU TIKET KONSER HINDIA=====")
        print("1. Login")
        print("2. Register")
        print("3. Konser tersedia")
        print("4. Keluar")

        pilihan = input("pilihan: ").strip()

        if pilihan == "1":
            akun = login()
            if akun is not None:
                masuk_sesuai_role(akun)
        elif pilihan == "2":
            register()
        elif pilihan == "3":
            tampilkan_kategori_tiket()
        elif pilihan == "4":
            print("Terima Kasih")
            break
        else:
            print("pilihan tidak valid")


if __name__ == "__main__":
    main()
