from bantuan import (MAKS_TIKET, buat_kode_pesanan, buat_kode_unik,
                     hitung_diskon, waktu_sekarang)
from database import (baca_data, file_konser, file_pembayaran, file_tiket,
                      simpan_data)

STATUS_AKTIF = ("Menunggu Pembayaran", "Menunggu Verifikasi", "Lunas")


def cari_pesanan(daftar, kode):
    return next((p for p in daftar if p["kode_pesan"] == kode), None)


def cari_kategori(konser, nomor):
    return next((k for k in konser["kategori"] if k["nomor"] == nomor), None)


def pembayaran_terakhir(kode):
    for bayar in reversed(baca_data(file_pembayaran)):
        if bayar["kode_pesan"] == kode:
            return bayar
    return None


def kembalikan_kuota(nama_kategori, jumlah):
    konser = baca_data(file_konser)
    for k in konser["kategori"]:
        if k["jenis"] == nama_kategori:
            k["kuota"] += jumlah
    simpan_data(file_konser, konser)


def buat_pesanan(username, nomor_kategori, jumlah):
    konser = baca_data(file_konser)
    daftar_tiket = baca_data(file_tiket)

    kategori = cari_kategori(konser, nomor_kategori)
    if kategori is None:
        raise ValueError("Kategori tidak valid")
    if not 1 <= jumlah <= MAKS_TIKET:
        raise ValueError(f"Jumlah tiket harus 1-{MAKS_TIKET}")
    if jumlah > kategori["kuota"]:
        raise ValueError("Kuota tidak cukup")

    harga_awal = kategori["harga"] * jumlah
    diskon = hitung_diskon(jumlah, harga_awal)

    pesanan = {
        "kode_pesan": buat_kode_pesanan(daftar_tiket),
        "username": username,
        "kategori": kategori["jenis"],
        "jumlah": jumlah,
        "harga_awal": harga_awal,
        "diskon": diskon,
        "total_bayar": harga_awal - diskon,
        "status": "Menunggu Pembayaran",
        "kode_unik": "",
        "status_tiket": "-",
        "waktu": waktu_sekarang(),
    }
    daftar_tiket.append(pesanan)
    simpan_data(file_tiket, daftar_tiket)

    kategori["kuota"] -= jumlah
    simpan_data(file_konser, konser)
    return pesanan


def setujui_pembayaran(kode):
    daftar_tiket = baca_data(file_tiket)
    daftar_bayar = baca_data(file_pembayaran)
    pesanan = cari_pesanan(daftar_tiket, kode)

    for bayar in daftar_bayar:
        if bayar["kode_pesan"] == kode and bayar["status"] == "Menunggu Verifikasi":
            bayar["status"] = "Terverifikasi"
    pesanan["status"] = "Lunas"
    pesanan["kode_unik"] = buat_kode_unik(daftar_tiket)
    pesanan["status_tiket"] = "Active"
    simpan_data(file_pembayaran, daftar_bayar)
    simpan_data(file_tiket, daftar_tiket)


def tolak_pembayaran(kode):
    daftar_tiket = baca_data(file_tiket)
    daftar_bayar = baca_data(file_pembayaran)
    pesanan = cari_pesanan(daftar_tiket, kode)

    for bayar in daftar_bayar:
        if bayar["kode_pesan"] == kode and bayar["status"] == "Menunggu Verifikasi":
            bayar["status"] = "Ditolak"
    pesanan["status"] = "Ditolak"
    simpan_data(file_pembayaran, daftar_bayar)
    simpan_data(file_tiket, daftar_tiket)
    kembalikan_kuota(pesanan["kategori"], pesanan["jumlah"])


def batalkan_pesanan(kode):
    daftar_tiket = baca_data(file_tiket)
    pesanan = cari_pesanan(daftar_tiket, kode)
    if pesanan is None:
        return
    pesanan["status"] = "Dibatalkan"
    pesanan["status_tiket"] = "-"
    simpan_data(file_tiket, daftar_tiket)
    kembalikan_kuota(pesanan["kategori"], pesanan["jumlah"])
