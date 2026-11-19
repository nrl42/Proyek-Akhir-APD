
from database import baca_data, file_konser
from bantuan import rupiah
from auth import login, register
from menu_user import menu_user
from menu_staff import menu_admin, menu_petugas


def tampilkan_info_konser():
    konser = baca_data(file_konser)
    print("\n==========")
    print(" ", konser["judul"])
    print("==========")
    print("tanggal : ", konser["tanggal"])
    print("waktu :", konser["waktu"])
    print("lokasi :", konser["lokasi"])

def tampilkan_kategori_tiket():
    konser = baca_data(file_konser)
    tampilkan_info_konser()
    print("\n kategori tiket yang tesedia:")
    for k in konser["kategori"]:
        print(f"-{k['jenis']}: {rupiah(k['harga'])} (sisa kuota:{k['kuota']})")

def masuk_sesuai_role(akun):
    if akun["role"] == "admin":
        menu_admin(akun)
    elif akun["role"] == "petugas":
        menu_petugas(akun)
    else:
        menu_user(akun)

def main():
    tampilkan_info_konser


    while True:
        if tampil_info:
            tampilkan_info_konser
            tampil_info = False

        print("\n=====MENU TIKET KONSER HINDIA=====")
        print("1. login")
        print("2. register")
        print("3. konser tersedia")
        print("4. logout")

        pilihan = input("pilihan: ")

        if pilihan == "1":
            akun = login()
            if akun is not None:
                masuk_sesuai_role(akun)
        elif pilihan == "2":
            register()

        elif pilihan == "3":
            tampilkan_kategori_tiket

        elif pilihan == "4":
            print("Terima Kasih")
            break

        else:
            print("pilihan tidak valid")


if __name__ == "__main__" :
    main()