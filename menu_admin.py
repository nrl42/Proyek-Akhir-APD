from database import (baca_data, simpan_data, file_akun, file_konser, file_diskon, file_tiket, file_pembayaran, file_pembatalan)
from bantuan import (rupiah, garis, input_angka, input_angka_kosong, input_wajib, tanya_ya_tidak, id_berikutnya, tampilkan_rincian, tampilkan_baris_pesanan, clear, input_password, tekan_enter)
from pesanan import (cari_pesanan, cari_kategori, pembayaran_terakhir, batalkan_pesanan)
from pembayaran import batalkan_kadaluarsa
from laporan import (hitung_penjualan, tampilkan_laporan, tampilkan_diagram_batang, simpan_laporan_teks, file_grafik, file_laporan)

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
        clear()
        daftar_akun = baca_data(file_akun)
        print("=====KELOLA AKUN=====")
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
                "password": input_password("Password: "),
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
                print(f"akun {a['username']} telah dihapus")
            else:
                print("penghapusan akun dibatalkan")
            tekan_enter()

        elif pilih == "4":
            print("Logout berhasil")
            return
        else:
            print("Inputan tidak valid")
            


def tampilkan_info_konser(konser):
    print("Judul   :", konser["judul"])
    print("Tanggal :", konser["tanggal"])
    print("Waktu   :", konser["waktu"])
    print("Lokasi  :", konser["lokasi"])


def tampilkan_katalog(konser):
    print(f"\n{'No':<4}{'Kategori':<12}{'Harga':>14}{'Sisa kuota':>12}")
    garis(42)
    for k in konser["kategori"]:
        print(f"{k['nomor']:<4}{k['jenis']:<12}{rupiah(k['harga']):>14}{k['kuota']:>12}")


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
    print("Kosongkan (Enter) jika tidak ingin mengubah.")
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
        print("=====KELOLA INFORMASI KONSER & KATALOG TIKET=====")
        tampilkan_info_konser(konser)
        tampilkan_katalog(konser)
        if pesan != "":
            print("\n>>", pesan)
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
    print(f"\n{'ID':<4}{'Nama':<22}{'Min':>5}{'Maks':>6}{'Persen':>8}")
    garis(45)
    for d in daftar_diskon:
        print(f"{d['id']:<4}{d['nama']:<22}{d['min_tiket']:>5}{d['maks_tiket']:>6}{d['persen']:>7}%")


def kelolaDiskon():
    while True:
        clear()
        daftar_diskon = baca_data(file_diskon)
        print("=====KELOLA KETENTUAN DISKON=====")
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
            

def lihatTransaksiPemesanan():
    clear()
    daftar_tiket = baca_data(file_tiket)
    print("=====SEMUA TRANSAKSI PEMESANAN=====")
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

def LihatTransaksiPembayaran():
    clear()
    daftar_bayar = baca_data(file_pembayaran)
    print("====== Transaksi Pembayaran ======")

    if len(daftar_bayar) == 0:
        print("transaksi pembayaran belum tersedia")
        return
        

    print(f"\n{'ID':<5}{'Kode':<15}{'Username':<15}{'Metode':<18}{'Nominal':<15}{'Status':<25}")

    for b in daftar_bayar:
        print(f"{b['id']:<5}{b['kode_pesan']:<15}" 
        f"{b['username']:<15}{b['metode']:<18}"
        f"{rupiah(b['nominal']):<15}{b['status']:<25}")

    tekan_enter()


def kelolaPembatalanTiket():
    while True:
        clear()
        daftar_batal = baca_data(file_pembatalan)
        menunggu = [b for b in daftar_batal if b["status"] == "Menunggu"]
        print("=====KELOLA PEMBATALAN TIKET=====")
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
    clear()
    daftar_tiket = baca_data(file_tiket)
    print("=====RINCIAN HARGA SEBELUM & SESUDAH DISKON=====")
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
    clear()
    hasil, pembeli = hitung_penjualan()
    total_tiket = sum(t for t, p in hasil.values())
    if total_tiket == 0:
        print("Laporan penjualan belum tersedia (belum ada transaksi lunas)")
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
        batalkan_kadaluarsa()
        clear()
        print("=== MENU ADMIN ===")
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
            print("Logout berhasil")
            break
        else:
            print("Menu tidak valid")