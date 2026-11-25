from database import (baca_data, simpan_data, file_akun, file_konser, file_diskon, file_tiket, file_pembayaran, file_pembatalan)
from bantuan import (rupiah, input_angka, input_angka_kosong, input_wajib, tanya_ya_tidak,
                     id_berikutnya, tampilkan_rincian, tampilkan_daftar_pesanan, clear,
                     input_password, tekan_enter, tabel, cetak_judul, sukses, gagal,
                     peringatan, info, warna_status)
from pesanan import (cari_pesanan, cari_kategori, pembayaran_terakhir, batalkan_pesanan)
from pembayaran import batalkan_kadaluarsa
from laporan import (hitung_penjualan, tampilkan_laporan, tampilkan_diagram_batang, simpan_laporan_teks, file_grafik, file_laporan)

ROLE_VALID = ("Admin", "Petugas", "User")


def tampilkan_akun(daftar_akun):
    tabel(["No", "Username", "Nama", "No HP", "Role"],
          [[nomor, a["username"], a["nama"], a["no_hp"], a["role"]]
           for nomor, a in enumerate(daftar_akun, start=1)])


def pilih_role():
    while True:
        for i, r in enumerate(ROLE_VALID, start=1):
            print(f"{i}. {r}")
        pilih = input_angka("Pilih role: ")
        if 1 <= pilih <= len(ROLE_VALID):
            return ROLE_VALID[pilih - 1]
        gagal("Role tidak valid")


def kelolaAkun(akun_admin):
    while True:
        clear()
        daftar_akun = baca_data(file_akun)
        cetak_judul("=====KELOLA AKUN=====")
        tampilkan_akun(daftar_akun)
        print("\n1. Tambah\n2. Ubah\n3. Hapus\n4. Keluar")
        pilih = input("Pilih: ").strip()

        if pilih == "1":
            username = input_wajib("Username: ")
            if username in {a["username"] for a in daftar_akun}:
                gagal("Username sudah dipakai!")
                tekan_enter()
                continue
            daftar_akun.append({
                "username": username,
                "password": input_password("Password: "),
                "nama": input_wajib("Nama: "),
                "no_hp": input_wajib("No HP: "),
                "role": pilih_role(),
            })
            simpan_data(file_akun, daftar_akun)
            sukses("Akun baru berhasil dibuat")
            tekan_enter()

        elif pilih == "2":
            nomor = input_angka("id akun yang diubah: ")
            if not 1 <= nomor <= len(daftar_akun):
                gagal("Pengguna tidak valid")
                tekan_enter()
                continue
            a = daftar_akun[nomor - 1]
            peringatan("Kosongkan (Enter) jika tidak ingin mengubah.")
            nama = input(f"Nama [{a['nama']}]: ").strip()
            password = input_password("Password baru: ")
            no_hp = input(f"No HP [{a['no_hp']}]: ").strip()
            if nama != "":
                a["nama"] = nama
            if password != "":
                a["password"] = password
            if no_hp != "":
                a["no_hp"] = no_hp
            if tanya_ya_tidak(f"Ubah role (sekarang {a['role']})?"):
                a["role"] = pilih_role()
            simpan_data(file_akun, daftar_akun)
            sukses("Data pengguna berhasil diubah")
            tekan_enter()

        elif pilih == "3":
            nomor = input_angka("id akun yang dihapus: ")
            if not 1 <= nomor <= len(daftar_akun):
                gagal("Pengguna tidak valid")
                tekan_enter()
                continue
            a = daftar_akun[nomor - 1]
            if a["username"] == akun_admin["username"]:
                gagal("Tidak bisa menghapus akun yang sedang dipakai!")
            elif tanya_ya_tidak(f"Hapus akun {a['username']}?"):
                daftar_akun.pop(nomor - 1)
                simpan_data(file_akun, daftar_akun)
                sukses(f"akun {a['username']} telah dihapus")
            else:
                peringatan("penghapusan akun dibatalkan")
            tekan_enter()

        elif pilih == "4":
            info("Kembali ke menu admin")
            return
        else:
            gagal("Inputan tidak valid")
            tekan_enter()


def tampilkan_info_konser(konser):
    tabel(["Keterangan", "Isi"], [
        ["Judul", konser["judul"]],
        ["Tanggal", konser["tanggal"]],
        ["Waktu", konser["waktu"]],
        ["Lokasi", konser["lokasi"]],
    ], judul="INFO KONSER")


def tampilkan_katalog(konser):
    tabel(["No", "Kategori", "Harga", "Sisa kuota"],
          [[k["nomor"], k["jenis"], rupiah(k["harga"]), k["kuota"]] for k in konser["kategori"]],
          judul="KATALOG TIKET")


def ubah_info_konser(konser):
    kunci = {1: "judul", 2: "tanggal", 3: "waktu", 4: "lokasi"}
    print("\n1. Judul\n2. Tanggal\n3. Waktu\n4. Lokasi\n0. Batal")
    pilih = input_angka("Pilih data yang diubah: ")
    if pilih == 0:
        return ""
    if pilih not in kunci:
        return "id tidak ditemukan"
    konser[kunci[pilih]] = input_wajib("Isi baru: ")
    simpan_data(file_konser, konser)
    return "Informasi konser berhasil diperbarui"


def tambah_kategori(konser):
    nama = input_wajib("Nama kategori: ")
    harga = input_angka("Harga: ")
    kuota = input_angka("Kuota: ")
    nama_ada = {k["jenis"].lower() for k in konser["kategori"]}
    if nama.lower() in nama_ada:
        return "Nama kategori harus unik"
    if harga <= 0 or kuota < 0:
        return "Harga harus > 0 dan kuota tidak boleh negatif"
    nomor_baru = max([k["nomor"] for k in konser["kategori"]] + [0]) + 1
    konser["kategori"].append(
        {"nomor": nomor_baru, "jenis": nama, "harga": harga, "kuota": kuota})
    simpan_data(file_konser, konser)
    return "Katalog baru berhasil ditambahkan"


def ubah_kategori(konser):
    kategori = cari_kategori(konser, input_angka("Nomor kategori yang diubah: "))
    if kategori is None:
        return "Kategori tidak ditemukan"
    peringatan("Kosongkan (Enter) jika tidak ingin mengubah.")
    nama = input(f"Nama [{kategori['jenis']}]: ").strip()
    harga = input_angka_kosong(f"Harga [{kategori['harga']}]: ")
    kuota = input_angka_kosong(f"Kuota [{kategori['kuota']}]: ")
    if harga == -1 or kuota == -1 or (harga is not None and harga <= 0) \
            or (kuota is not None and kuota < 0):
        return "Data tidak valid, perubahan dibatalkan"
    if nama != "":
        kategori["jenis"] = nama
    if harga is not None:
        kategori["harga"] = harga
    if kuota is not None:
        kategori["kuota"] = kuota
    simpan_data(file_konser, konser)
    return "Katalog berhasil diperbarui"


def hapus_kategori(konser):
    kategori = cari_kategori(konser, input_angka("Nomor kategori yang dihapus: "))
    if kategori is None:
        return "Kategori tidak ditemukan"
    aktif = [t for t in baca_data(file_tiket)
             if t["kategori"] == kategori["jenis"] and t["status"] in ("Menunggu Pembayaran", "Menunggu Verifikasi", "Lunas")]
    if len(aktif) > 0:
        return "Kategori tidak bisa dihapus, masih ada pesanan aktif."
    if tanya_ya_tidak(f"Hapus kategori {kategori['jenis']}?"):
        konser["kategori"].remove(kategori)
        simpan_data(file_konser, konser)
        return "Kategori berhasil dihapus"
    return ""


def kelolaKonserDanKatalog():
    pesan = ""
    while True:
        clear()
        konser = baca_data(file_konser)
        cetak_judul("=====KELOLA INFORMASI KONSER & KATALOG TIKET=====")
        tampilkan_info_konser(konser)
        tampilkan_katalog(konser)
        if pesan != "":
            info("\n>> " + pesan)
            pesan = ""
        print("\n1. Ubah informasi konser")
        print("2. Tambah kategori tiket")
        print("3. Ubah kategori tiket")
        print("4. Hapus kategori tiket")
        print("0. Keluar")
        pilih = input("Pilih aksi: ").strip()

        if pilih == "1":
            pesan = ubah_info_konser(konser)
        elif pilih == "2":
            pesan = tambah_kategori(konser)
        elif pilih == "3":
            pesan = ubah_kategori(konser)
        elif pilih == "4":
            pesan = hapus_kategori(konser)
        elif pilih == "0":
            return
        else:
            pesan = "Pilihan tidak valid"


def tampilkan_diskon(daftar_diskon):
    tabel(["ID", "Nama", "Min", "Maks", "Persen"],
          [[d["id"], d["nama"], d["min_tiket"], d["maks_tiket"], f"{d['persen']}%"]
           for d in daftar_diskon])


def kelolaDiskon():
    while True:
        clear()
        daftar_diskon = baca_data(file_diskon)
        cetak_judul("=====KELOLA KETENTUAN DISKON=====")
        tampilkan_diskon(daftar_diskon)
        print("\n1. Tambah\n2. Ubah\n3. Hapus\n4. Keluar")
        pilih = input("Pilih aksi: ").strip()

        if pilih == "1":
            nama = input_wajib("Nama diskon: ")
            minimal = input_angka("Minimal pembelian tiket: ")
            maksimal = input_angka("Maksimal pembelian tiket: ")
            persen = input_angka("Persentase diskon (0-100): ")
            if minimal < 1 or maksimal < minimal or not 0 <= persen <= 100:
                gagal("Data tidak valid (jumlah tiket / persen 0-100)")
            else:
                daftar_diskon.append({"id": id_berikutnya(daftar_diskon), "nama": nama,
                                      "min_tiket": minimal, "maks_tiket": maksimal,
                                      "persen": persen})
                simpan_data(file_diskon, daftar_diskon)
                sukses("Diskon baru berhasil disimpan")
            tekan_enter()

        elif pilih == "2":
            id_diskon = input_angka("ID diskon yang diubah: ")
            diskon = None
            for d in daftar_diskon:
                if d["id"] == id_diskon:
                    diskon = d
            if diskon is None:
                gagal("Diskon tidak ditemukan")
                tekan_enter()
                continue
            peringatan("Kosongkan (Enter) jika tidak ingin mengubah.")
            nama = input(f"Nama [{diskon['nama']}]: ").strip()
            minimal = input_angka_kosong(f"Minimal tiket [{diskon['min_tiket']}]: ")
            maksimal = input_angka_kosong(f"Maksimal tiket [{diskon['maks_tiket']}]: ")
            persen = input_angka_kosong(f"Persen [{diskon['persen']}]: ")

            minimal_baru = diskon["min_tiket"] if minimal is None else minimal
            maksimal_baru = diskon["maks_tiket"] if maksimal is None else maksimal
            persen_baru = diskon["persen"] if persen is None else persen
            if -1 in (minimal, maksimal, persen) or minimal_baru < 1 \
                    or maksimal_baru < minimal_baru or not 0 <= persen_baru <= 100:
                gagal("Data tidak valid, perubahan dibatalkan")
                tekan_enter()
                continue
            if nama != "":
                diskon["nama"] = nama
            diskon["min_tiket"] = minimal_baru
            diskon["maks_tiket"] = maksimal_baru
            diskon["persen"] = persen_baru
            simpan_data(file_diskon, daftar_diskon)
            sukses("Ketentuan diskon berhasil diperbarui")
            tekan_enter()

        elif pilih == "3":
            id_diskon = input_angka("ID diskon yang dihapus: ")
            diskon = None
            for d in daftar_diskon:
                if d["id"] == id_diskon:
                    diskon = d
            if diskon is None:
                gagal("Diskon tidak ditemukan")
            elif tanya_ya_tidak(f"Hapus {diskon['nama']}?"):
                daftar_diskon.remove(diskon)
                simpan_data(file_diskon, daftar_diskon)
                sukses("Ketentuan diskon berhasil dihapus")
            tekan_enter()

        elif pilih == "4":
            return
        else:
            gagal("Pilihan tidak valid")
            tekan_enter()


def lihatTransaksiPemesanan():
    clear()
    daftar_tiket = baca_data(file_tiket)
    cetak_judul("=====SEMUA TRANSAKSI PEMESANAN=====")
    if len(daftar_tiket) == 0:
        peringatan("Transaksi belum tersedia")
        tekan_enter()
        return

    tampilkan_daftar_pesanan(daftar_tiket)

    while True:
        kode = input("Kode pemesanan untuk detail (0 untuk kembali): ").strip().upper()
        if kode == "0":
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
            ["Kode unik", t["kode_unik"] if t["kode_unik"] else "-"],
            ["Status", warna_status(t["status"])],
            ["Status tiket", warna_status(t["status_tiket"])],
        ], judul="DETAIL TRANSAKSI")


def LihatTransaksiPembayaran():
    clear()
    daftar_bayar = baca_data(file_pembayaran)

    if len(daftar_bayar) == 0:
        cetak_judul("====== TRANSAKSI PEMBAYARAN ======")
        peringatan("transaksi pembayaran belum tersedia")
        tekan_enter()
        return

    tabel(["ID", "Kode", "Username", "Metode", "Nominal", "Status"],
          [[b["id"], b["kode_pesan"], b["username"], b["metode"],
            rupiah(b["nominal"]), warna_status(b["status"])] for b in daftar_bayar],
          judul="TRANSAKSI PEMBAYARAN")
    tekan_enter()


def kelolaPembatalanTiket():
    while True:
        clear()
        daftar_batal = baca_data(file_pembatalan)
        menunggu = [b for b in daftar_batal if b["status"] == "Menunggu"]
        if len(menunggu) == 0:
            cetak_judul("=====KELOLA PEMBATALAN TIKET=====")
            peringatan("Belum ada permintaan pembatalan")
            tekan_enter()
            return

        tabel(["ID", "Kode pesan", "Username", "Alasan"],
              [[b["id"], b["kode_pesan"], b["username"], b["alasan"]] for b in menunggu],
              judul="KELOLA PEMBATALAN TIKET")

        id_batal = input_angka("Masukkan ID permintaan (0 untuk kembali): ")
        if id_batal == 0:
            return

        permintaan = None
        for b in menunggu:
            if b["id"] == id_batal:
                permintaan = b
        if permintaan is None:
            gagal("ID tidak valid")
            tekan_enter()
            continue

        pesanan = cari_pesanan(baca_data(file_tiket), permintaan["kode_pesan"])
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


def lihatRincianHarga():
    clear()
    daftar_tiket = baca_data(file_tiket)
    cetak_judul("=====RINCIAN HARGA SEBELUM & SESUDAH DISKON=====")
    if len(daftar_tiket) == 0:
        peringatan("Belum ada data pemesanan")
        tekan_enter()
        return

    tampilkan_daftar_pesanan(daftar_tiket)

    kode = input("Kode pemesanan (0 untuk kembali): ").strip().upper()
    if kode == "0":
        return
    t = cari_pesanan(daftar_tiket, kode)
    if t is None:
        gagal("Transaksi tidak ditemukan")
        tekan_enter()
        return

    persen = t["diskon"] * 100 // t["harga_awal"] if t["harga_awal"] else 0
    tampilkan_rincian(t)
    info("Persentase diskon: " + str(persen) + "%")
    tekan_enter()


def lihatLaporanPenjualan():
    clear()
    hasil, pembeli = hitung_penjualan()
    total_tiket = sum(t for t, p in hasil.values())
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
    while True:
        batalkan_kadaluarsa()
        clear()
        cetak_judul("=== MENU ADMIN ===")
        print("Selamat datang,", akun["nama"])
        print("1. Kelola akun")
        print("2. Kelola informasi konser dan katalog tiket")
        print("3. Kelola ketentuan diskon pembelian tiket")
        print("4. Lihat seluruh transaksi pemesanan")
        print("5. Lihat Transaksi Pembayaran")
        print("6. Kelola pembatalan tiket")
        print("7. Lihat rincian harga sebelum dan sesudah diskon")
        print("8. Lihat laporan penjualan tiket (diagram batang)")
        print("9. Logout")
        menu = input("Input menu: ").strip()

        if menu == "1":
            kelolaAkun(akun)
        elif menu == "2":
            kelolaKonserDanKatalog()
        elif menu == "3":
            kelolaDiskon()
        elif menu == "4":
            lihatTransaksiPemesanan()
        elif menu == "5":
            LihatTransaksiPembayaran()
        elif menu == "6":
            kelolaPembatalanTiket()
        elif menu == "7":
            lihatRincianHarga()
        elif menu == "8":
            lihatLaporanPenjualan()
        elif menu == "9":
            sukses("Logout berhasil")
            break
        else:
            gagal("Menu tidak valid")
            tekan_enter()
