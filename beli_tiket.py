from bantuan import (MAKS_TIKET, clear, gagal, hitung_diskon, info,
                     input_angka_kosong, persen_diskon, rupiah, sukses, tabel,
                     tampilkan_rincian, tanya_ya_tidak, warna_status)
from database import baca_data, file_konser
from pembayaran import bayar_pesanan
from pesanan import buat_pesanan, cari_kategori


def pilih_kategori(konser):
    while True:
        clear()
        tabel(["No", "Jenis", "Harga", "Sisa kuota"],
              [[k["nomor"], k["jenis"], rupiah(k["harga"]), k["kuota"]]
               for k in konser["kategori"]],
              judul="PILIH KATEGORI TIKET")

        nomor = input_angka_kosong("Pilih nomor kategori (Enter untuk kembali): ")
        if nomor is None:
            return None

        kategori = cari_kategori(konser, nomor)
        if kategori is not None:
            return kategori

        gagal("maaf kategori tidak valid")
        input("Tekan Enter untuk coba lagi...")


def input_jumlah(kategori):
    """Mengembalikan jumlah tiket, atau None jika Enter (kembali)."""
    while True:
        jumlah = input_angka_kosong(
            f"Input jumlah tiket (maks {MAKS_TIKET}, Enter untuk kembali): ")
        if jumlah is None:
            return None
        if 1 <= jumlah <= MAKS_TIKET and jumlah <= kategori["kuota"]:
            return jumlah
        gagal(f"jumlah tidak valid (maks {MAKS_TIKET} tiket) atau kuota tidak cukup")


def proses_pemesanan(username):
    konser = baca_data(file_konser)

    kategori = pilih_kategori(konser)
    if kategori is None:
        return
    jumlah = input_jumlah(kategori)
    if jumlah is None:
        return

    harga_awal = kategori["harga"] * jumlah
    info(f"\nDiskon yang berlaku: {persen_diskon(jumlah)}% "
         f"({rupiah(hitung_diskon(jumlah, harga_awal))})")

    try:
        pesanan = buat_pesanan(username, kategori["nomor"], jumlah)
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
