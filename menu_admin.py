from bantuan import (cetak_judul, cetak_menu, clear, gagal, id_berikutnya, info,
                     input_angka, input_angka_kosong, input_no_hp, input_password,
                     input_wajib, peringatan, rupiah, sukses, tabel,
                     tampilkan_daftar_pesanan, tampilkan_info_konser,
                     tampilkan_katalog, tampilkan_rincian, tanya_ya_tidak,
                     tekan_enter, warna_status)
from database import (baca_data, file_akun, file_diskon, file_konser,
                      file_pembatalan, file_pembayaran, file_tiket, simpan_data)
from laporan import (file_grafik, file_laporan, hitung_penjualan, hitung_total,
                     simpan_laporan_teks, tampilkan_diagram_batang,
                     tampilkan_laporan)
from menu_petugas import LihatDataPemesanan
from pembayaran import batalkan_kadaluarsa
from pesanan import (STATUS_AKTIF, batalkan_pesanan, cari_kategori,
                     cari_pesanan)

ROLE_VALID = ("Admin", "Petugas", "User")
PETUNJUK_KOSONG = "Kosongkan (Enter) jika tidak ingin mengubah."

OPSI_MENU = [
    "Kelola akun",
    "Kelola informasi konser dan katalog tiket",
    "Kelola ketentuan diskon pembelian tiket",
    "Lihat seluruh transaksi pemesanan",
    "Lihat Transaksi Pembayaran",
    "Kelola pembatalan tiket",
    "Lihat data pemesanan",
    "Lihat laporan penjualan tiket (diagram batang)",
    "Logout",
]


def tampilkan_akun(daftar_akun):
    tabel(["No", "Username", "Nama", "No HP", "Role"],
          [[no, a["username"], a["nama"], a["no_hp"], a["role"]]
           for no, a in enumerate(daftar_akun, start=1)])


def pilih_role():
    while True:
        cetak_menu(ROLE_VALID)
        pilihan = input_angka("Pilih role: ")
        if 1 <= pilihan <= len(ROLE_VALID):
            return ROLE_VALID[pilihan - 1]
        gagal("Role tidak valid")


def pilih_akun(daftar_akun, pesan):
    nomor = input_angka_kosong(pesan)
    if nomor is None:
        return None
    if not 1 <= nomor <= len(daftar_akun):
        gagal("Pengguna tidak valid")
        tekan_enter()
        return None
    return daftar_akun[nomor - 1]


def tambah_akun(daftar_akun):
    username = input_wajib("Username: ")
    if username in {a["username"] for a in daftar_akun}:
        gagal("Username sudah dipakai!")
        tekan_enter()
        return

    password = ""
    while password == "":
        password = input_password("Password: ")
        if password == "":
            gagal("Password tidak boleh kosong!")

    daftar_akun.append({
        "username": username,
        "password": password,
        "nama": input_wajib("Nama: "),
        "no_hp": input_no_hp("No HP: "),
        "role": pilih_role(),
    })
    simpan_data(file_akun, daftar_akun)
    sukses("Akun baru berhasil dibuat")
    tekan_enter()


def ubah_akun(daftar_akun):
    akun = pilih_akun(daftar_akun, "Nomor akun yang diubah (Enter untuk kembali): ")
    if akun is None:
        return

    peringatan(PETUNJUK_KOSONG)
    nama = input(f"Nama [{akun['nama']}]: ").strip()
    password = input_password("Password baru: ")
    no_hp = input_no_hp(f"No HP [{akun['no_hp']}]: ", boleh_kosong=True)

    if nama:
        akun["nama"] = nama
    if password:
        akun["password"] = password
    if no_hp:
        akun["no_hp"] = no_hp
    if tanya_ya_tidak(f"Ubah role (sekarang {akun['role']})?"):
        akun["role"] = pilih_role()

    simpan_data(file_akun, daftar_akun)
    sukses("Data pengguna berhasil diubah")
    tekan_enter()


def hapus_akun(daftar_akun, akun_admin):
    akun = pilih_akun(daftar_akun, "Nomor akun yang dihapus (Enter untuk kembali): ")
    if akun is None:
        return

    if akun["username"] == akun_admin["username"]:
        gagal("Tidak bisa menghapus akun yang sedang dipakai!")
    elif tanya_ya_tidak(f"Hapus akun {akun['username']}?"):
        daftar_akun.remove(akun)
        simpan_data(file_akun, daftar_akun)
        sukses(f"akun {akun['username']} telah dihapus")
    else:
        peringatan("penghapusan akun dibatalkan")
    tekan_enter()


def kelolaAkun(akun_admin):
    while True:
        clear()
        daftar_akun = baca_data(file_akun)
        cetak_judul("=====KELOLA AKUN=====")
        tampilkan_akun(daftar_akun)
        print()
        cetak_menu(["Tambah", "Ubah", "Hapus", "Keluar"])
        pilihan = input("Pilih: ").strip()

        if pilihan == "1":
            tambah_akun(daftar_akun)
        elif pilihan == "2":
            ubah_akun(daftar_akun)
        elif pilihan == "3":
            hapus_akun(daftar_akun, akun_admin)
        elif pilihan == "4":
            info("Kembali ke menu admin")
            return
        else:
            gagal("Inputan tidak valid")
            tekan_enter()


def ubah_info_konser(konser):
    kunci = {1: "judul", 2: "tanggal", 3: "waktu", 4: "lokasi"}
    print()
    cetak_menu(["Judul", "Tanggal", "Waktu", "Lokasi"])
    pilihan = input_angka_kosong("Pilih data yang diubah (Enter untuk batal): ")
    if pilihan is None:
        return ""
    if pilihan not in kunci:
        return "Pilihan tidak valid"
    konser[kunci[pilihan]] = input_wajib("Isi baru: ")
    simpan_data(file_konser, konser)
    return "Informasi konser berhasil diperbarui"


def tambah_kategori(konser):
    nama = input("Nama kategori (Enter untuk batal): ").strip()
    if nama == "":
        return ""
    if nama.lower() in {k["jenis"].lower() for k in konser["kategori"]}:
        return "Nama kategori harus unik"

    harga = input_angka("Harga: ")
    kuota = input_angka("Kuota: ")
    if harga <= 0 or kuota < 0:
        return "Harga harus > 0 dan kuota tidak boleh negatif"

    nomor_baru = max((k["nomor"] for k in konser["kategori"]), default=0) + 1
    konser["kategori"].append(
        {"nomor": nomor_baru, "jenis": nama, "harga": harga, "kuota": kuota})
    simpan_data(file_konser, konser)
    return "Katalog baru berhasil ditambahkan"


def ubah_kategori(konser):
    nomor = input_angka_kosong("Nomor kategori yang diubah (Enter untuk batal): ")
    if nomor is None:
        return ""
    kategori = cari_kategori(konser, nomor)
    if kategori is None:
        return "Kategori tidak ditemukan"

    peringatan(PETUNJUK_KOSONG)
    nama = input(f"Nama [{kategori['jenis']}]: ").strip()
    harga = input_angka_kosong(f"Harga [{kategori['harga']}]: ")
    kuota = input_angka_kosong(f"Kuota [{kategori['kuota']}]: ")

    if harga == -1 or kuota == -1 or (harga is not None and harga <= 0) \
            or (kuota is not None and kuota < 0):
        return "Data tidak valid, perubahan dibatalkan"

    if nama and nama != kategori["jenis"]:
        if nama.lower() in {k["jenis"].lower() for k in konser["kategori"]}:
            return "Nama kategori harus unik, perubahan dibatalkan"
        if any(t["kategori"] == kategori["jenis"] for t in baca_data(file_tiket)):
            return "Nama kategori tidak bisa diubah karena sudah ada pesanan"
        kategori["jenis"] = nama
    if harga is not None:
        kategori["harga"] = harga
    if kuota is not None:
        kategori["kuota"] = kuota

    simpan_data(file_konser, konser)
    return "Katalog berhasil diperbarui"


def hapus_kategori(konser):
    nomor = input_angka_kosong("Nomor kategori yang dihapus (Enter untuk batal): ")
    if nomor is None:
        return ""
    kategori = cari_kategori(konser, nomor)
    if kategori is None:
        return "Kategori tidak ditemukan"

    if any(t["kategori"] == kategori["jenis"] and t["status"] in STATUS_AKTIF
           for t in baca_data(file_tiket)):
        return "Kategori tidak bisa dihapus, masih ada pesanan aktif."

    if tanya_ya_tidak(f"Hapus kategori {kategori['jenis']}?"):
        konser["kategori"].remove(kategori)
        simpan_data(file_konser, konser)
        return "Kategori berhasil dihapus"
    return ""


def kelolaKonserDanKatalog():
    aksi = {
        "1": ubah_info_konser,
        "2": tambah_kategori,
        "3": ubah_kategori,
        "4": hapus_kategori,
    }
    pesan = ""
    while True:
        clear()
        konser = baca_data(file_konser)
        cetak_judul("=====KELOLA INFORMASI KONSER & KATALOG TIKET=====")
        tampilkan_info_konser(konser)
        tampilkan_katalog(konser)
        if pesan:
            info("\n>> " + pesan)
            pesan = ""

        print()
        cetak_menu(["Ubah informasi konser", "Tambah kategori tiket",
                    "Ubah kategori tiket", "Hapus kategori tiket"])
        print("Enter. Keluar")
        pilihan = input("Pilih aksi: ").strip()

        if pilihan == "":
            return
        if pilihan in aksi:
            pesan = aksi[pilihan](konser)
        else:
            pesan = "Pilihan tidak valid"


def tampilkan_diskon(daftar_diskon):
    tabel(["ID", "Nama", "Min", "Maks", "Persen"],
          [[d["id"], d["nama"], d["min_tiket"], d["maks_tiket"], f"{d['persen']}%"]
           for d in daftar_diskon])


def diskon_valid(minimal, maksimal, persen):
    return 1 <= minimal <= maksimal and 0 <= persen <= 100


def pilih_diskon(daftar_diskon, pesan):
    """Minta ID diskon. None jika Enter atau tidak ditemukan."""
    id_diskon = input_angka_kosong(pesan)
    if id_diskon is None:
        return None
    diskon = next((d for d in daftar_diskon if d["id"] == id_diskon), None)
    if diskon is None:
        gagal("Diskon tidak ditemukan")
        tekan_enter()
    return diskon


def tambah_diskon(daftar_diskon):
    nama = input_wajib("Nama diskon: ")
    minimal = input_angka("Minimal pembelian tiket: ")
    maksimal = input_angka("Maksimal pembelian tiket: ")
    persen = input_angka("Persentase diskon (0-100): ")

    if diskon_valid(minimal, maksimal, persen):
        daftar_diskon.append({"id": id_berikutnya(daftar_diskon), "nama": nama,
                              "min_tiket": minimal, "maks_tiket": maksimal,
                              "persen": persen})
        simpan_data(file_diskon, daftar_diskon)
        sukses("Diskon baru berhasil disimpan")
    else:
        gagal("Data tidak valid (jumlah tiket / persen 0-100)")
    tekan_enter()


def ubah_diskon(daftar_diskon):
    diskon = pilih_diskon(daftar_diskon, "ID diskon yang diubah (Enter untuk kembali): ")
    if diskon is None:
        return

    peringatan(PETUNJUK_KOSONG)
    nama = input(f"Nama [{diskon['nama']}]: ").strip()
    minimal = input_angka_kosong(f"Minimal tiket [{diskon['min_tiket']}]: ")
    maksimal = input_angka_kosong(f"Maksimal tiket [{diskon['maks_tiket']}]: ")
    persen = input_angka_kosong(f"Persen [{diskon['persen']}]: ")

    if -1 in (minimal, maksimal, persen):
        gagal("Data tidak valid, perubahan dibatalkan")
        tekan_enter()
        return

    minimal = diskon["min_tiket"] if minimal is None else minimal
    maksimal = diskon["maks_tiket"] if maksimal is None else maksimal
    persen = diskon["persen"] if persen is None else persen
    if not diskon_valid(minimal, maksimal, persen):
        gagal("Data tidak valid, perubahan dibatalkan")
        tekan_enter()
        return

    if nama:
        diskon["nama"] = nama
    diskon["min_tiket"], diskon["maks_tiket"], diskon["persen"] = minimal, maksimal, persen
    simpan_data(file_diskon, daftar_diskon)
    sukses("Ketentuan diskon berhasil diperbarui")
    tekan_enter()


def hapus_diskon(daftar_diskon):
    diskon = pilih_diskon(daftar_diskon, "ID diskon yang dihapus (Enter untuk kembali): ")
    if diskon is None:
        return

    if tanya_ya_tidak(f"Hapus {diskon['nama']}?"):
        daftar_diskon.remove(diskon)
        simpan_data(file_diskon, daftar_diskon)
        sukses("Ketentuan diskon berhasil dihapus")
    tekan_enter()


def kelolaDiskon():
    while True:
        clear()
        daftar_diskon = baca_data(file_diskon)
        cetak_judul("=====KELOLA KETENTUAN DISKON=====")
        tampilkan_diskon(daftar_diskon)
        print()
        cetak_menu(["Tambah", "Ubah", "Hapus", "Keluar"])
        pilihan = input("Pilih aksi: ").strip()

        if pilihan == "1":
            tambah_diskon(daftar_diskon)
        elif pilihan == "2":
            ubah_diskon(daftar_diskon)
        elif pilihan == "3":
            hapus_diskon(daftar_diskon)
        elif pilihan == "4":
            return
        else:
            gagal("Pilihan tidak valid")
            tekan_enter()


def lihatTransaksiPemesanan():
    clear()
    daftar_tiket = baca_data(file_tiket)
    cetak_judul("=====SEMUA TRANSAKSI PEMESANAN=====")
    if not daftar_tiket:
        peringatan("Transaksi belum tersedia")
        tekan_enter()
        return

    tampilkan_daftar_pesanan(daftar_tiket)

    while True:
        kode = input("Kode pemesanan untuk detail (Enter untuk kembali): ").strip().upper()
        if kode == "":
            return
        t = cari_pesanan(daftar_tiket, kode)
        if t is None:
            gagal("Transaksi tidak ditemukan")
            continue
        tabel(["Keterangan", "Isi"], [
            ["Kode pesan", t["kode_pesan"]],
            ["Pelanggan", t["username"]],
            ["Kategori", f"{t['kategori']} x {t['jumlah']}"],
            ["Total bayar", rupiah(t["total_bayar"])],
            ["Kode unik", t["kode_unik"] or "-"],
            ["Status", warna_status(t["status"])],
            ["Status tiket", warna_status(t["status_tiket"])],
        ], judul="DETAIL TRANSAKSI")


def LihatTransaksiPembayaran():
    clear()
    daftar_bayar = baca_data(file_pembayaran)

    if not daftar_bayar:
        cetak_judul("====== TRANSAKSI PEMBAYARAN ======")
        peringatan("transaksi pembayaran belum tersedia")
    else:
        tabel(["ID", "Kode", "Username", "Metode", "Nominal", "Status"],
              [[b["id"], b["kode_pesan"], b["username"], b.get("metode", "-"),
                rupiah(b["nominal"]), warna_status(b["status"])] for b in daftar_bayar],
              judul="TRANSAKSI PEMBAYARAN")
    tekan_enter()


def kelolaPembatalanTiket():
    while True:
        clear()
        daftar_batal = baca_data(file_pembatalan)
        menunggu = [b for b in daftar_batal if b["status"] == "Menunggu"]
        if not menunggu:
            cetak_judul("=====KELOLA PEMBATALAN TIKET=====")
            peringatan("Belum ada permintaan pembatalan")
            tekan_enter()
            return

        tabel(["ID", "Kode pesan", "Username", "Alasan"],
              [[b["id"], b["kode_pesan"], b["username"], b["alasan"]] for b in menunggu],
              judul="KELOLA PEMBATALAN TIKET")

        id_batal = input_angka_kosong("Masukkan ID permintaan (Enter untuk kembali): ")
        if id_batal is None:
            return

        permintaan = next((b for b in menunggu if b["id"] == id_batal), None)
        if permintaan is None:
            gagal("ID tidak valid")
            tekan_enter()
            continue

        pesanan = cari_pesanan(baca_data(file_tiket), permintaan["kode_pesan"])

        if pesanan is None or pesanan["status"] not in STATUS_AKTIF \
                or pesanan["status_tiket"] == "Used":
            permintaan["status"] = "Ditolak"
            simpan_data(file_pembatalan, daftar_batal)
            peringatan("Pesanan sudah tidak aktif / tiket sudah dipakai, "
                       "permintaan otomatis ditolak")
            tekan_enter()
            continue

        tampilkan_rincian(pesanan)
        print("Status :", warna_status(pesanan["status"]))
        print("Alasan :", permintaan["alasan"])

        if tanya_ya_tidak("Setujui pembatalan?"):
            batalkan_pesanan(permintaan["kode_pesan"])
            permintaan["status"] = "Disetujui"
            sukses("Pembatalan berhasil disetujui, kuota dikembalikan")
        else:
            permintaan["status"] = "Ditolak"
            peringatan("Pembatalan ditolak, tiket tetap berlaku")
        simpan_data(file_pembatalan, daftar_batal)

        if not tanya_ya_tidak("Proses permintaan lain?"):
            return


def lihatLaporanPenjualan():
    clear()
    hasil, pembeli = hitung_penjualan()
    total_tiket, _ = hitung_total(hasil)
    if total_tiket == 0:
        peringatan("Laporan penjualan belum tersedia (belum ada transaksi lunas)")
        tekan_enter()
        return

    tampilkan_laporan(hasil, pembeli)
    info("\nMenampilkan diagram batang...")
    tampilkan_diagram_batang(hasil)
    info("Grafik tersimpan di: " + file_grafik)

    if tanya_ya_tidak("Cetak/unduh laporan ke file?"):
        simpan_laporan_teks(hasil, pembeli)
        sukses("Laporan tersimpan di: " + file_laporan)
    tekan_enter()


def menu_admin(akun):
    aksi = {
        "1": lambda: kelolaAkun(akun),
        "2": kelolaKonserDanKatalog,
        "3": kelolaDiskon,
        "4": lihatTransaksiPemesanan,
        "5": LihatTransaksiPembayaran,
        "6": kelolaPembatalanTiket,
        "7": LihatDataPemesanan,
        "8": lihatLaporanPenjualan,
    }
    while True:
        batalkan_kadaluarsa()
        clear()
        cetak_judul("=== MENU ADMIN ===")
        print("Selamat datang,", akun["nama"])
        cetak_menu(OPSI_MENU)
        pilihan = input("Input menu: ").strip()

        if pilihan == "9":
            sukses("Logout berhasil")
            break
        if pilihan in aksi:
            aksi[pilihan]()
        else:
            gagal("Menu tidak valid")
            tekan_enter()
