from database import (baca_data, simpan_data, file_tiket, file_konser,
                    file_pembayaran)
from bantuan import (buat_kode_pesanan, buat_kode_unik, hitung_diskon,
                    id_berikutnya, waktu_sekarang, MAKS_TIKET)


def cari_pesanan(daftar, kode):
    for p in daftar:
        if p["kode_pesan"] == kode:
            return p
    return None


def cari_kategori(konser, nomor):
    for k in konser["kategori"]:
        if k["nomor"] == nomor:
            return k
    return None


def pembayaran_terakhir(kode):
    hasil = None
    for b in baca_data(file_pembayaran):
        if b["kode_pesan"] == kode:
            hasil = b
    return hasil


def kembalikan_kuota(nama_kategori, jumlah):
    konser = baca_data(file_konser)
    for k in konser["kategori"]:
        if k["jenis"] == nama_kategori:
            k["kuota"] = k["kuota"] + jumlah
    simpan_data(file_konser, konser)


def buat_pesanan(username, nomor_kategori, jumlah):
    konser = baca_data(file_konser)
    daftar_tiket = baca_data(file_tiket)

    kategori = cari_kategori(konser, nomor_kategori)
    if kategori is None:
        raise ValueError("Kategori tidak valid")
    if jumlah < 1 or jumlah > MAKS_TIKET:
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

    kategori["kuota"] = kategori["kuota"] - jumlah
    simpan_data(file_konser, konser)
    return pesanan


def kirim_pembayaran(kode, nominal):
    daftar_tiket = baca_data(file_tiket)
    daftar_bayar = baca_data(file_pembayaran)

    pesanan = cari_pesanan(daftar_tiket, kode)
    if pesanan is None:
        raise ValueError("Pesanan tidak ditemukan")
    if pesanan["status"] != "Menunggu Pembayaran":
        raise ValueError("Pesanan ini tidak sedang menunggu pembayaran")
    if nominal != pesanan["total_bayar"]:
        raise ValueError("Nominal tidak sesuai dengan total bayar")

    daftar_bayar.append({
        "id": id_berikutnya(daftar_bayar),
        "kode_pesan": kode,
        "username": pesanan["username"],
        "nominal": nominal,
        "waktu": waktu_sekarang(),
        "status": "Menunggu Verifikasi",
    })
    pesanan["status"] = "Menunggu Verifikasi"
    simpan_data(file_pembayaran, daftar_bayar)
    simpan_data(file_tiket, daftar_tiket)


def setujui_pembayaran(kode):
    daftar_tiket = baca_data(file_tiket)
    daftar_bayar = baca_data(file_pembayaran)
    pesanan = cari_pesanan(daftar_tiket, kode)

    for b in daftar_bayar:
        if b["kode_pesan"] == kode and b["status"] == "Menunggu Verifikasi":
            b["status"] = "Terverifikasi"
    pesanan["status"] = "Lunas"
    pesanan["kode_unik"] = buat_kode_unik(daftar_tiket)
    pesanan["status_tiket"] = "Active"
    simpan_data(file_pembayaran, daftar_bayar)
    simpan_data(file_tiket, daftar_tiket)


def tolak_pembayaran(kode):
    daftar_tiket = baca_data(file_tiket)
    daftar_bayar = baca_data(file_pembayaran)
    pesanan = cari_pesanan(daftar_tiket, kode)

    for b in daftar_bayar:
        if b["kode_pesan"] == kode and b["status"] == "Menunggu Verifikasi":
            b["status"] = "Ditolak"
    pesanan["status"] = "Ditolak"
    simpan_data(file_pembayaran, daftar_bayar)
    simpan_data(file_tiket, daftar_tiket)
    kembalikan_kuota(pesanan["kategori"], pesanan["jumlah"])


def batalkan_pesanan(kode):
    daftar_tiket = baca_data(file_tiket)
    pesanan = cari_pesanan(daftar_tiket, kode)
    pesanan["status"] = "Dibatalkan"
    pesanan["status_tiket"] = "-"
    simpan_data(file_tiket, daftar_tiket)
    kembalikan_kuota(pesanan["kategori"], pesanan["jumlah"])
