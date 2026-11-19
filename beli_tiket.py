from database import baca_data, simpan-data, file_tiket, file_konser
from bantuan import rupiah, buat_kode_pesanan, buat_kode_unik

def input_angka(pesan):
    try:
        return int(input(pesan))
    except ValueError:
        return 0

def pilih_kategori(konser):
    while True:
        print("\n=====Pilih kategori tiket=====")
        for k in konser["kategori"]:
            print(f"{k['nomor']}. {k['jenis']} {k['harga']} (sisa kuota: {k['kuota']})")

        kategori = input_angka("input kategori : ")

        for k in konser["kategori"]:
            if k["nomor"] == kategori:
                return k

        print("maaf kategori tidak valid")

def input_jumlah(kategori_dipilih):
    while True:
        jumlah = input_angka("Input jumlah tiket: ")

        if jumlah >= 1 and jumlah <= 4 and jumlah <= kategori_dipilih["kuota"]:
            return jumlah

            print("jumlah tidak valid maks 4 tiket ")

def hitung_diskon(jumlah, harga_awal):
    if jumlah >= 3 and jumlah <= 4:
        diskon = harga_awal * 10 // 100
    elif jumlah == 2:
        diskon = harga_awal * 5 // 100
    else:
        diskon = 0
    return diskon

def tampilkan_rincian(pesanan):
    print("\n=====RINCIAN PEMESANAN=====")
    print("Kategori   :", pesanan["kategori"])
    print("Jumlah     :", pesanan["jumlah"])
    print("Harga awal :", rupiah(pesanan["harga_awal"]))
    print("Diskon     :", rupiah(pesanan["diskon"]))
    print("Total bayar:", rupiah(pesanan["total_bayar"]))

def tampilkan_struk(pesanan):
    print("\n===============")
    print("STRUK PEMESANAN")
    print("===============")
    print("Kode pesan :", pesanan["kode_pesan"])
    print("Kode unik  :", pesanan["kode_unik"])
    print("Pemesan    :", pesanan["username"])
    print("Kategori   :", pesanan["kategori"])
    print("Jumlah     :", pesanan["jumlah"])
    print("Harga awal :", rupiah(pesanan["harga_awal"]))
    print("Diskon     :", rupiah(pesanan["diskon"]))
    print("Total bayar:", rupiah(pesanan["total_bayar"]))
    print("Status     :", pesanan["status"])
    print("===============")

def beli_tiket(akun):
    konser = baca_data(file_konser)
    daftar_tiket = baca_data(file_tiket)

    kategori_dipilih = pilih_kategori(konser)
    jumlah = input_jumlah(kategori_dipilih)

    kategori_dipilih = pilih_kategori(konser)
    jumlah = input_jumlah(kategori_dipilih)

    pesanan = {
        "kode_pesan": buat_kode_pesan(daftar_tiket),   # generate otomatis
        "username": akun["username"],
        "kategori": kategori_dipilih["jenis"],
        "jumlah": jumlah,
        "harga_awal": harga_awal,
        "diskon": diskon,
        "total_bayar": total_bayar,
        "status": "Menunggu Pembayaran",
        "kode_unik": ""
    }
    tampilkan_rincian(pesanan)

    daftar_tiket.append(pesanan)
    simpan_data(file_tiket, daftar_tiket)

    kategori_dipilih["kuota"] = kategori_dipilih["kuota"] - jumlah
    simpan_data(file_konser, konser)

    print("\nKode pesan Anda:", pesanan["kode_pesan"])
    print("Status:", pesanan["status"])

    print("\n=====PEMBAYARA=====")
    while True:
        nominal = input_angka("Masukkan nominal pembayaran (" + rupiah(total_bayar) + "): ")
        if nominal == total_bayar:
            break
        print("Nominal tidak sesuai dengan total bayar anda")

    pesanan["kode_unik"] = buat_kode_unik()
    pesanan["status"] = "Lunas"
    simpan_data(file_tiket, daftar_tiket)

    tampilkan_struk(pesanan)