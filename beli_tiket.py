from database import baca_data, file_konser
from bantuan import (clear, rupiah, input_angka, tanya_ya_tidak, tampilkan_rincian, hitung_diskon, persen_diskon, tabel, gagal, sukses, info, warna_status, MAKS_TIKET)
from pesanan import cari_kategori, buat_pesanan

from pembayaran import bayar_pesanan


def pilih_kategori(konser):
    while True:
        clear()
        tabel(["No", "Jenis", "Harga", "Sisa kuota"],
              [[k["nomor"], k["jenis"], rupiah(k["harga"]), k["kuota"]]
               for k in konser["kategori"]],
              judul="PILIH KATEGORI TIKET")
        print("0. Kembali")

        nomor = input_angka("input kategori : ")
        if nomor == 0:
            return None

        kategori = cari_kategori(konser, nomor)
        if kategori is not None:
            return kategori

        gagal("maaf kategori tidak valid")
        input("Tekan Enter untuk coba lagi...")


def input_jumlah(kategori_dipilih):
    while True:
        jumlah = input_angka(f"Input jumlah tiket (maks {MAKS_TIKET}, 0 untuk kembali): ")
        if jumlah == 0:
            return None
        if 1 <= jumlah <= MAKS_TIKET and jumlah <= kategori_dipilih["kuota"]:
            return jumlah
        gagal(f"jumlah tidak valid (maks {MAKS_TIKET} tiket) atau kuota tidak cukup")


def proses_pemesanan(username):
    konser = baca_data(file_konser)

    kategori_dipilih = pilih_kategori(konser)
    if kategori_dipilih is None:
        return
    jumlah = input_jumlah(kategori_dipilih)
    if jumlah is None:
        return

    harga_awal = kategori_dipilih["harga"] * jumlah
    info(f"\nDiskon yang berlaku: {persen_diskon(jumlah)}% "
         f"({rupiah(hitung_diskon(jumlah, harga_awal))})")

    try:
        pesanan = buat_pesanan(username, kategori_dipilih["nomor"], jumlah)
    except ValueError as error:
        gagal("Pemesanan gagal: " + str(error))
        return

    clear()
    tampilkan_rincian(pesanan)
    sukses("\nKode pesan Anda: " + pesanan["kode_pesan"])
    print("Status:", warna_status(pesanan["status"]))

    if tanya_ya_tidak("Bayar sekarang?"):
        bayar_pesanan(pesanan["kode_pesan"])
    else:
        info("Pesanan bisa dibayar nanti lewat menu Bayar Pesanan.")


def beli_tiket(akun):
    proses_pemesanan(akun["username"])