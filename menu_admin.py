from database import (baca_data, simpan_data, file_akun, file_konser, file_diskon,
                    file_tiket, file_pembayaran, file_pembatalan)
from bantuan import (rupiah, garis, input_angka, input_angka_kosong, input_wajib,
                    tanya_ya_tidak, id_berikutnya, tampilkan_rincian,
                    tampilkan_baris_pesanan)
from pesanan import (cari_pesanan, pembayaran_terakhir, setujui_pembayaran,
                    tolak_pembayaran, batalkan_pesanan)
from laporan import (hitung_penjualan, tampilkan_laporan, tampilkan_diagram_batang,
                    simpan_laporan_teks, file_grafik, file_laporan)

ROLE_VALID = ("Admin", "Petugas", "User")

def tampilkan_akun(daftar_akun):
    print(f"\n{'No':<4}{'Username':<15}{'Nama':<20}{'No HP':<15}{'Role':<8}")
    garis(62)
    for nomor, a in enumerate(daftar_akun, start=1):
        print(f"{nomor:<4}{a['username']:<15}{a['nama']:<20}{a['no_hp']:<15}{a['role']:<8}")


def pilih_role():
    while True:
        for i, r in enumerate(ROLE_VALID, start=1):
            print(f"{i}. {r}")
        pilih = input_angka("Pilih role: ")
        if 1 <= pilih <= len(ROLE_VALID):
            return ROLE_VALID[pilih - 1]
        print("Role tidak valid")


def kelolaAkun(akun_admin):
    while True:
        daftar_akun = baca_data(file_akun)
        print("\n=====KELOLA AKUN=====")
        tampilkan_akun(daftar_akun)
        print("\n1. Tambah\n2. Ubah\n3. Hapus\n4. Keluar")
        pilih = input("Pilih: ").strip()

        if pilih == "1":
            username = input_wajib("Username: ")
            if username in {a["username"] for a in daftar_akun}:   
                print("Username sudah dipakai!")
                continue
            daftar_akun.append({
                "username": username,
                "password": input_wajib("Password: "),
                "nama": input_wajib("Nama: "),
                "no_hp": input_wajib("No HP: "),
                "role": pilih_role(),
            })
            simpan_data(file_akun, daftar_akun)
            print("Akun baru berhasil dibuat")

        elif pilih == "2":
            nomor = input_angka("id akun yang diubah: ")
            if not 1 <= nomor <= len(daftar_akun):
                print("Pengguna tidak valid")
                continue
            a = daftar_akun[nomor - 1]
            print("Kosongkan (Enter) jika tidak ingin mengubah.")
            nama = input(f"Nama [{a['nama']}]: ").strip()
            password = input("Password baru: ").strip()
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
            print("Data pengguna berhasil diubah")

        elif pilih == "3":
            nomor = input_angka("id akun yang dihapus: ")
            if not 1 <= nomor <= len(daftar_akun):
                print("Pengguna tidak valid")
                continue
            a = daftar_akun[nomor - 1]
            if a["username"] == akun_admin["username"]:
                print("Tidak bisa menghapus akun yang sedang dipakai!")
            elif tanya_ya_tidak(f"Hapus akun {a['username']}?"):
                daftar_akun.pop(nomor - 1)
                simpan_data(file_akun, daftar_akun)
                print("Akun berhasil dihapus")

        elif pilih == "4":
            print("Logout berhasil")
            return
        else:
            print("Inputan tidak valid")


def kelolaInformasiKonser():
    while True:
        konser = baca_data(file_konser)
        print("\n=====KELOLA INFORMASI KONSER=====")
        print("1. Judul   :", konser["judul"])
        print("2. Tanggal :", konser["tanggal"])
        print("3. Waktu   :", konser["waktu"])
        print("4. Lokasi  :", konser["lokasi"])
        print("0. Keluar")

        pilih = input_angka("Pilih data yang diubah: ")
        kunci = {1: "judul", 2: "tanggal", 3: "waktu", 4: "lokasi"}   

        if pilih == 0:
            return
        if pilih not in kunci:
            print("id tidak ditemukan")
            continue

        konser[kunci[pilih]] = input_wajib("Isi baru: ")
        simpan_data(file_konser, konser)
        print("informasi konser berhasil diperbarui")



def tampilkan_katalog(konser):
    print(f"\n{'No':<4}{'Kategori':<12}{'Harga':>14}{'Sisa kuota':>12}")
    garis(42)
    for k in konser["kategori"]:
        print(f"{k['nomor']:<4}{k['jenis']:<12}{rupiah(k['harga']):>14}{k['kuota']:>12}")


def kelolaKatalog():
    while True:
        konser = baca_data(file_konser)
        print("\n=====KELOLA KATALOG TIKET=====")
        tampilkan_katalog(konser)
        print("\n1. Tambah\n2. Ubah\n3. Hapus\n4. Keluar")
        pilih = input("Pilih aksi: ").strip()

        if pilih == "1":
            nama = input_wajib("Nama kategori: ")
            nama_ada = {k["jenis"].lower() for k in konser["kategori"]}
            harga = input_angka("Harga: ")
            kuota = input_angka("Kuota: ")
            if nama.lower() in nama_ada:
                print("Nama kategori harus unik")
            elif harga <= 0 or kuota < 0:
                print("Harga harus > 0 dan kuota tidak boleh negatif")
            else:
                nomor_baru = max([k["nomor"] for k in konser["kategori"]] + [0]) + 1
                konser["kategori"].append(
                    {"nomor": nomor_baru, "jenis": nama, "harga": harga, "kuota": kuota})
                simpan_data(file_konser, konser)
                print("Katalog baru berhasil ditambahkan")

        elif pilih == "2":
            nomor = input_angka("Nomor kategori yang diubah: ")
            kategori = None
            for k in konser["kategori"]:
                if k["nomor"] == nomor:
                    kategori = k
            if kategori is None:
                print("Kategori tidak ditemukan")
                continue
            print("Kosongkan (Enter) jika tidak ingin mengubah.")
            nama = input(f"Nama [{kategori['jenis']}]: ").strip()
            harga = input_angka_kosong(f"Harga [{kategori['harga']}]: ")
            kuota = input_angka_kosong(f"Kuota [{kategori['kuota']}]: ")
            if harga == -1 or kuota == -1 or (harga is not None and harga <= 0) \
                    or (kuota is not None and kuota < 0):
                print("Data tidak valid, perubahan dibatalkan")
                continue
            if nama != "":
                kategori["jenis"] = nama
            if harga is not None:
                kategori["harga"] = harga
            if kuota is not None:
                kategori["kuota"] = kuota
            simpan_data(file_konser, konser)
            print("Katalog berhasil diperbarui")

        elif pilih == "3":
            nomor = input_angka("Nomor kategori yang dihapus: ")
            kategori = None
            for k in konser["kategori"]:
                if k["nomor"] == nomor:
                    kategori = k
            if kategori is None:
                print("Kategori tidak ditemukan")
                continue
            aktif = [t for t in baca_data(file_tiket)
                    if t["kategori"] == kategori["jenis"]
                    and t["status"] in ("Menunggu Pembayaran", "Menunggu Verifikasi", "Lunas")]
            if len(aktif) > 0:
                print("Kategori tidak bisa dihapus, masih ada pesanan aktif.")
            elif tanya_ya_tidak(f"Hapus kategori {kategori['jenis']}?"):
                konser["kategori"].remove(kategori)
                simpan_data(file_konser, konser)
                print("Kategori berhasil dihapus")

        elif pilih == "4":
            return
        else:
            print("Pilihan tidak valid")



def tampilkan_diskon(daftar_diskon):
    print(f"\n{'ID':<4}{'Nama':<22}{'Min':>5}{'Maks':>6}{'Persen':>8}")
    garis(45)
    for d in daftar_diskon:
        print(f"{d['id']:<4}{d['nama']:<22}{d['min_tiket']:>5}{d['maks_tiket']:>6}{d['persen']:>7}%")


def kelolaDiskon():
    while True:
        daftar_diskon = baca_data(file_diskon)
        print("\n=====KELOLA KETENTUAN DISKON=====")
        tampilkan_diskon(daftar_diskon)
        print("\n1. Tambah\n2. Ubah\n3. Hapus\n4. Keluar")
        pilih = input("Pilih aksi: ").strip()

        if pilih == "1":
            nama = input_wajib("Nama diskon: ")
            minimal = input_angka("Minimal pembelian tiket: ")
            maksimal = input_angka("Maksimal pembelian tiket: ")
            persen = input_angka("Persentase diskon (0-100): ")
            if minimal < 1 or maksimal < minimal or not 0 <= persen <= 100:
                print("Data tidak valid (jumlah tiket / persen 0-100)")
            else:
                daftar_diskon.append({"id": id_berikutnya(daftar_diskon), "nama": nama,
                                    "min_tiket": minimal, "maks_tiket": maksimal,
                                    "persen": persen})
                simpan_data(file_diskon, daftar_diskon)
                print("Diskon baru berhasil disimpan")

        elif pilih == "2":
            id_diskon = input_angka("ID diskon yang diubah: ")
            diskon = None
            for d in daftar_diskon:
                if d["id"] == id_diskon:
                    diskon = d
            if diskon is None:
                print("Diskon tidak ditemukan")
                continue
            print("Kosongkan (Enter) jika tidak ingin mengubah.")
            nama = input(f"Nama [{diskon['nama']}]: ").strip()
            minimal = input_angka_kosong(f"Minimal tiket [{diskon['min_tiket']}]: ")
            maksimal = input_angka_kosong(f"Maksimal tiket [{diskon['maks_tiket']}]: ")
            persen = input_angka_kosong(f"Persen [{diskon['persen']}]: ")

            minimal_baru = diskon["min_tiket"] if minimal is None else minimal
            maksimal_baru = diskon["maks_tiket"] if maksimal is None else maksimal
            persen_baru = diskon["persen"] if persen is None else persen
            if -1 in (minimal, maksimal, persen) or minimal_baru < 1 \
                    or maksimal_baru < minimal_baru or not 0 <= persen_baru <= 100:
                print("Data tidak valid, perubahan dibatalkan")
                continue
            if nama != "":
                diskon["nama"] = nama
            diskon["min_tiket"] = minimal_baru
            diskon["maks_tiket"] = maksimal_baru
            diskon["persen"] = persen_baru
            simpan_data(file_diskon, daftar_diskon)
            print("Ketentuan diskon berhasil diperbarui")

        elif pilih == "3":
            id_diskon = input_angka("ID diskon yang dihapus: ")
            diskon = None
            for d in daftar_diskon:
                if d["id"] == id_diskon:
                    diskon = d
            if diskon is None:
                print("Diskon tidak ditemukan")
            elif tanya_ya_tidak(f"Hapus {diskon['nama']}?"):
                daftar_diskon.remove(diskon)
                simpan_data(file_diskon, daftar_diskon)
                print("Ketentuan diskon berhasil dihapus")

        elif pilih == "4":
            return
        else:
            print("Pilihan tidak valid")

def lihatDataPelanggan():
    pelanggan = [a for a in baca_data(file_akun) if a["role"].lower() == "user"]
    print("\n=====DATA PELANGGAN=====")
    if len(pelanggan) == 0:
        print("Data pelanggan belum tersedia")
        return

    for nomor, a in enumerate(pelanggan, start=1):
        print(f"{nomor}. {a['username']} | {a['nama']} | {a['no_hp']}")

    while True:
        nomor = input_angka("Pilih nomor pelanggan untuk rincian (0 untuk kembali): ")
        if nomor == 0:
            return
        if not 1 <= nomor <= len(pelanggan):
            print("Nomor tidak valid")
            continue

        a = pelanggan[nomor - 1]
        pesanan_user = [t for t in baca_data(file_tiket) if t["username"] == a["username"]]
        lunas = [t for t in pesanan_user if t["status"] == "Lunas"]
        print("\n--- Rincian Pelanggan ---")
        print("Username      :", a["username"])
        print("Nama          :", a["nama"])
        print("No HP         :", a["no_hp"])
        print("Jumlah pesanan:", len(pesanan_user))
        print("Total belanja :", rupiah(sum(t["total_bayar"] for t in lunas)))



def lihatTransaksiPemesanan():
    daftar_tiket = baca_data(file_tiket)
    print("\n=====SEMUA TRANSAKSI PEMESANAN=====")
    if len(daftar_tiket) == 0:
        print("Transaksi belum tersedia")
        return

    for t in daftar_tiket:
        tampilkan_baris_pesanan(t)

    while True:
        kode = input("Kode pemesanan untuk detail (0 untuk kembali): ").strip().upper()
        if kode == "0":
            return
        t = cari_pesanan(daftar_tiket, kode)
        if t is None:
            print("Transaksi tidak ditemukan")
            continue
        print("\n--- Detail Transaksi ---")
        print("Kode pesan   :", t["kode_pesan"])
        print("Pelanggan    :", t["username"])
        print("Kategori     :", t["kategori"], "x", t["jumlah"])
        print("Total bayar  :", rupiah(t["total_bayar"]))
        print("Kode unik    :", t["kode_unik"] if t["kode_unik"] else "-")
        print("Status       :", t["status"])
        print("Status tiket :", t["status_tiket"])



def kelolaVerifikasiPembayaran():
    while True:
        menunggu = [b for b in baca_data(file_pembayaran) if b["status"] == "Menunggu Verifikasi"]
        print("\n=====VERIFIKASI PEMBAYARAN=====")
        if len(menunggu) == 0:
            print("Tidak ada pembayaran menunggu")
            return

        for b in menunggu:
            print(f"{b['kode_pesan']} | {b['username']} | {rupiah(b['nominal'])} | {b['waktu']}")

        kode = input("Kode pesanan yang diperiksa (0 untuk kembali): ").strip().upper()
        if kode == "0":
            return

        bayar = None
        for b in menunggu:
            if b["kode_pesan"] == kode:
                bayar = b
        if bayar is None:
            print("kode pesanan tidak ada")
            continue

        pesanan = cari_pesanan(baca_data(file_tiket), kode)
        print("\n--- Detail Pembayaran ---")
        tampilkan_rincian(pesanan)
        print("Nominal dibayar:", rupiah(bayar["nominal"]))

        if bayar["nominal"] != pesanan["total_bayar"]:
            print("PERINGATAN: nominal tidak sama dengan total bayar!")

        if tanya_ya_tidak("Setujui pembayaran?"):
            setujui_pembayaran(kode)
            print("Pembayaran berhasil diverifikasi, status Lunas, tiket Active")
        else:
            tolak_pembayaran(kode)
            print("Pembayaran ditolak")

        if not tanya_ya_tidak("Verifikasi transaksi lain?"):
            return



def kelolaPembatalanTiket():
    while True:
        daftar_batal = baca_data(file_pembatalan)
        menunggu = [b for b in daftar_batal if b["status"] == "Menunggu"]
        print("\n=====KELOLA PEMBATALAN TIKET=====")
        if len(menunggu) == 0:
            print("Belum ada permintaan pembatalan")
            return

        for b in menunggu:
            print(f"ID {b['id']} | {b['kode_pesan']} | {b['username']} | alasan: {b['alasan']}")

        id_batal = input_angka("Masukkan ID permintaan (0 untuk kembali): ")
        if id_batal == 0:
            return

        permintaan = None
        for b in menunggu:
            if b["id"] == id_batal:
                permintaan = b
        if permintaan is None:
            print("ID tidak valid")
            continue

        pesanan = cari_pesanan(baca_data(file_tiket), permintaan["kode_pesan"])
        print("\n--- Detail Pemesanan ---")
        tampilkan_rincian(pesanan)
        print("Status    :", pesanan["status"])
        print("Alasan    :", permintaan["alasan"])

        if tanya_ya_tidak("Setujui pembatalan?"):
            batalkan_pesanan(permintaan["kode_pesan"])
            permintaan["status"] = "Disetujui"
            print("Pembatalan berhasil disetujui, kuota dikembalikan")
        else:
            permintaan["status"] = "Ditolak"
            print("Pembatalan ditolak, tiket tetap berlaku")
        simpan_data(file_pembatalan, daftar_batal)

        if not tanya_ya_tidak("Proses permintaan lain?"):
            return



def lihatRincianHarga():
    daftar_tiket = baca_data(file_tiket)
    print("\n=====RINCIAN HARGA SEBELUM & SESUDAH DISKON=====")
    if len(daftar_tiket) == 0:
        print("Belum ada data pemesanan")
        return

    for t in daftar_tiket:
        tampilkan_baris_pesanan(t)

    kode = input("Kode pemesanan (0 untuk kembali): ").strip().upper()
    if kode == "0":
        return
    t = cari_pesanan(daftar_tiket, kode)
    if t is None:
        print("Transaksi tidak ditemukan")
        return

    persen = t["diskon"] * 100 // t["harga_awal"] if t["harga_awal"] else 0
    tampilkan_rincian(t)
    print("Persentase diskon:", str(persen) + "%")


def lihatLaporanPenjualan():
    hasil, pembeli = hitung_penjualan()
    total_tiket = sum(t for t, p in hasil.values())
    if total_tiket == 0:
        print("\nLaporan penjualan belum tersedia (belum ada transaksi lunas)")
        return

    tampilkan_laporan(hasil, pembeli)
    print("\nMenampilkan diagram batang...")
    tampilkan_diagram_batang(hasil)
    print("Grafik tersimpan di:", file_grafik)

    if tanya_ya_tidak("Cetak/unduh laporan ke file?"):
        simpan_laporan_teks(hasil, pembeli)
        print("Laporan tersimpan di:", file_laporan)


def menu_admin(akun):
    while True:
        print("\n=== MENU ADMIN ===")
        print("Selamat datang,", akun["nama"])
        print("1. Kelola akun")
        print("2. Kelola informasi konser")
        print("3. Kelola katalog (kategori, harga, kuota)")
        print("4. Kelola ketentuan diskon pembelian tiket")
        print("5. Lihat data pelanggan")
        print("6. Lihat seluruh transaksi pemesanan")
        print("7. Kelola dan verifikasi pembayaran")
        print("8. Kelola pembatalan tiket")
        print("9. Lihat rincian harga sebelum dan sesudah diskon")
        print("10. Lihat laporan penjualan tiket (diagram batang)")
        print("11. Logout")
        menu = input("Input menu: ").strip()

        if menu == "1":
            kelolaAkun(akun)
        elif menu == "2":
            kelolaInformasiKonser()
        elif menu == "3":
            kelolaKatalog()
        elif menu == "4":
            kelolaDiskon()
        elif menu == "5":
            lihatDataPelanggan()
        elif menu == "6":
            lihatTransaksiPemesanan()
        elif menu == "7":
            kelolaVerifikasiPembayaran()
        elif menu == "8":
            kelolaPembatalanTiket()
        elif menu == "9":
            lihatRincianHarga()
        elif menu == "10":
            lihatLaporanPenjualan()
        elif menu == "11":
            print("Logout berhasil")
            break
        else:
            print("Menu tidak valid")
