from datetime import datetime, timedelta

from database import baca_data, simpan_data, file_tiket, file_pembayaran
from bantuan import (clear, rupiah, input_angka, input_wajib, tampilkan_struk, tabel, tekan_enter, id_berikutnya, waktu_sekarang, PrettyTable)
from pesanan import cari_pesanan, setujui_pembayaran, batalkan_pesanan

METODE_PEMBAYARAN = ("Transfer BCA",)
REKENING_TUJUAN = {"bank": "BCA", "nomor": "1234567890", "atas_nama": "Panitia Konser Hindia"}
BATAS_MENIT = 15
FORMAT_WAKTU = "%Y-%m-%d %H:%M:%S"


def sisa_detik(pesanan):
    try:
        mulai = datetime.strptime(pesanan["waktu"], FORMAT_WAKTU)
    except (ValueError, KeyError):
        return BATAS_MENIT * 60          # data waktu rusak: anggap belum habis
    batas = mulai + timedelta(minutes=BATAS_MENIT)
    return int((batas - datetime.now()).total_seconds())


def format_sisa(detik):
    detik = max(detik, 0)
    return f"{detik // 60:02d}:{detik % 60:02d}"


def batalkan_kadaluarsa():
    """Batalkan semua pesanan 'Menunggu Pembayaran' yang lewat 15 menit.
    batalkan_pesanan() mengembalikan kuota. Mengembalikan daftar kode yang dibatalkan."""
    kadaluarsa = [t["kode_pesan"] for t in baca_data(file_tiket)
                if t["status"] == "Menunggu Pembayaran" and sisa_detik(t) <= 0]
    for kode in kadaluarsa:
        batalkan_pesanan(kode)
    return kadaluarsa


def ambil_pesanan_aktif(kode):
    """Ambil pesanan yang masih boleh dibayar, atau None (dengan pesan alasannya)."""
    if kode in batalkan_kadaluarsa():
        print(f"Batas waktu pembayaran ({BATAS_MENIT} menit) habis. " "Pesanan otomatis dibatalkan dan kuota dikembalikan.")
        return None
    pesanan = cari_pesanan(baca_data(file_tiket), kode)
    if pesanan is None:
        print("Pesanan tidak ditemukan")
        return None
    if pesanan["status"] != "Menunggu Pembayaran":
        print("Pesanan ini tidak bisa dibayar (status:", pesanan["status"] + ")")
        return None
    return pesanan


def isi_data_diri(pesanan):
    print("\n=====DATA PEMESAN & PEMILIK TIKET=====")
    print("(ketik 0 pada nama pemesan untuk bayar nanti)")
    nama = input_wajib("Nama pemesan : ")
    if nama == "0":
        return None

    while True:
        no_hp = input_wajib("No HP pemesan : ")
        if no_hp.isdigit() and 11 <= len(no_hp) <= 13 and no_hp.startswith("08") :
            break
        print("No HP harus 11-13 digit angka dan diawali 08")

    while True:
        email = input_wajib("Email : ")
        if "@" in email and "." in email.split("@")[-1]:
            break
        print("Format email tidak valid")

    pemilik = []
    for i in range(1, pesanan["jumlah"] + 1):
        pemilik.append(input_wajib(f"Nama pemilik tiket {i} : "))

    return {"nama_pemesan": nama, "no_hp": no_hp, "email": email,
            "pemilik_tiket": pemilik}


def simpan_data_diri(kode, data):
    daftar_tiket = baca_data(file_tiket)
    pesanan = cari_pesanan(daftar_tiket, kode)
    pesanan["data_diri"] = data
    simpan_data(file_tiket, daftar_tiket)


def pilih_metode():
    while True:
        print("\n=====PILIH METODE PEMBAYARAN=====")
        for nomor, metode in enumerate(METODE_PEMBAYARAN, start=1):
            print(f"{nomor}. {metode}")
        print("0. Bayar nanti")

        pilihan = input_angka("Pilih metode: ")
        if pilihan == 0:
            return None
        if 1 <= pilihan <= len(METODE_PEMBAYARAN):
            return METODE_PEMBAYARAN[pilihan - 1]
        print("Metode tidak valid")


def catat_pembayaran(pesanan, metode):
    daftar_bayar = baca_data(file_pembayaran)
    daftar_bayar.append({
        "id": id_berikutnya(daftar_bayar),
        "kode_pesan": pesanan["kode_pesan"],
        "username": pesanan["username"],
        "metode": metode,
        "nominal": pesanan["total_bayar"],
        "waktu": waktu_sekarang(),
        "status": "Menunggu Verifikasi",
    })
    simpan_data(file_pembayaran, daftar_bayar)

    daftar_tiket = baca_data(file_tiket)
    cari_pesanan(daftar_tiket, pesanan["kode_pesan"])["status"] = "Menunggu Verifikasi"
    simpan_data(file_tiket, daftar_tiket)


def input_nominal(pesan):
    """Terima '270000', '270.000', 'Rp270.000', 'Rp 270.000', dll.
    Mengembalikan angka (int), atau None kalau bukan angka."""
    teks = input(pesan).strip().lower()
    for buang in ("rp", ".", ",", " "):
        teks = teks.replace(buang, "")
    try:
        return int(teks)
    except ValueError:
        return None


def proses_pembayaran(pesanan, metode):
    """Mengembalikan 'berhasil', 'ditunda', atau 'gagal' (kadaluarsa/status berubah)."""
    kode = pesanan["kode_pesan"]
    while True:
        clear()
        tabel(["Keterangan", "Isi"], [
            ["Kode pesan", kode],
            ["Metode", metode],
            ["Bank", REKENING_TUJUAN["bank"]],
            ["No. rekening", REKENING_TUJUAN["nomor"]],
            ["Atas nama", REKENING_TUJUAN["atas_nama"]],
            ["Nominal transfer", rupiah(pesanan["total_bayar"])],
            ["Sisa waktu", format_sisa(sisa_detik(pesanan))],
        ], judul="TUJUAN TRANSFER")

        nominal = input_nominal("Masukkan nominal yang ditransfer "
                                "(contoh: 270000 atau Rp270.000, 0 untuk bayar nanti): ")
        if nominal == 0:
            return "ditunda"
        if nominal is None:
            print("Nominal harus berupa angka. Contoh: 270000 atau Rp270.000")
            tekan_enter()
            continue

        if ambil_pesanan_aktif(kode) is None:
            return "gagal"

        if nominal != pesanan["total_bayar"]:
            print("Nominal tidak sesuai dengan total bayar, coba lagi.")
            tekan_enter()
            continue
        break

    catat_pembayaran(pesanan, metode)
    setujui_pembayaran(kode)
    return "berhasil"


def tampilkan_eticket(kode, metode):
    pesanan = cari_pesanan(baca_data(file_tiket), kode)
    clear()
    print("===== PEMBAYARAN BERHASIL - E-TICKET =====")
    tampilkan_struk(pesanan)
    print("Metode     :", metode)
    data = pesanan.get("data_diri")
    if data:
        tabel(["No", "Nama Pemilik Tiket"], [[i, nama] for i, nama in enumerate(data["pemilik_tiket"], start=1)], judul="PEMILIK TIKET")
        print("Pemesan :", data["nama_pemesan"], "|", data["no_hp"], "|", data["email"])


def bayar_pesanan(kode):
    clear()
    pesanan = ambil_pesanan_aktif(kode)
    if pesanan is None:
        tekan_enter()
        return

    print(f"Selesaikan pembayaran dalam {BATAS_MENIT} menit sejak pesan "
        f"(sisa {format_sisa(sisa_detik(pesanan))}).")

    if "data_diri" not in pesanan:
        data = isi_data_diri(pesanan)
        if data is None:
            print("Pembayaran ditunda. Pesanan bisa dibayar lewat menu Bayar Pesanan.")
            tekan_enter()
            return
        simpan_data_diri(kode, data)

    metode = pilih_metode()
    if metode is None:
        print("Pembayaran ditunda. Pesanan bisa dibayar lewat menu Bayar Pesanan.")
        tekan_enter()
        return

    pesanan = ambil_pesanan_aktif(kode)
    if pesanan is None:
        tekan_enter()
        return

    hasil = proses_pembayaran(pesanan, metode)
    if hasil == "berhasil":
        tampilkan_eticket(kode, metode)
    elif hasil == "ditunda":
        print("Pembayaran belum dilakukan. Selesaikan sebelum batas waktu habis.")
    tekan_enter()