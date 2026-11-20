from database import baca_data, simpan_data, file_akun, file_tiket, file_konser
from bantuan import rupiah, buat_kode_unik

ROLE_VALID = ["admin", "petugas", "user"]
MAKS_TIKET = 4
ATURAN_DISKON_DEFAULT = [
    {"min_tiket": 2, "maks_tiket": 2, "persen": 5},
    {"min_tiket": 3, "maks_tiket": 4, "persen": 10},
]
STATUS_AKTIF = ("Lunas", "Menunggu Pembayaran")


# =====================================================
# FUNGSI BANTU
# =====================================================
def input_angka(pesan):
    """Untuk input menu. Input salah dianggap 0."""
    try:
        return int(input(pesan))
    except ValueError:
        return 0


def baca_angka(pesan):
    """Untuk input nilai. Input salah mengembalikan None."""
    try:
        return int(input(pesan))
    except ValueError:
        print("Input harus berupa angka")
        return None


def input_teks(pesan):
    while True:
        teks = input(pesan).strip()
        if teks:
            return teks
        print("Input tidak boleh kosong")


def konfirmasi(pesan):
    return input(pesan + " (y/n): ").strip().lower() == "y"


def cari_kategori(konser, jenis):
    for k in konser.get("kategori", []):
        if k["jenis"] == jenis:
            return k
    return None


def cari_kategori_nomor(konser, nomor):
    for k in konser.get("kategori", []):
        if k["nomor"] == nomor:
            return k
    return None


def cari_pesanan(daftar, kode):
    for p in daftar:
        if str(p["kode_pesan"]).lower() == kode.lower():
            return p
    return None


def tampilkan_tabel_pesanan(daftar):
    print(f"{'Kode':<12}{'Pemesan':<14}{'Kategori':<10}{'Jml':<5}{'Total':<14}{'Status':<20}")
    print("-" * 75)
    for p in daftar:
        print(f"{str(p['kode_pesan']):<12}{p['username']:<14}{p['kategori']:<10}"
              f"{p['jumlah']:<5}{rupiah(p['total_bayar']):<14}{p['status']:<20}")


def ambil_aturan_diskon(konser):
    aturan = konser.get("diskon")
    if aturan is None:
        aturan = [dict(a) for a in ATURAN_DISKON_DEFAULT]
    return aturan


# =====================================================
# 1. KELOLA AKUN
# =====================================================
def tampilkan_akun(daftar_akun):
    print("\n=====DAFTAR AKUN=====")
    if not daftar_akun:
        print("Belum ada akun")
        return
    print(f"{'No':<4}{'Username':<20}{'Role':<10}")
    for i, a in enumerate(daftar_akun, 1):
        print(f"{i:<4}{a['username']:<20}{a.get('role', 'user'):<10}")


def cari_akun(daftar_akun, username):
    for a in daftar_akun:
        if a["username"] == username:
            return a
    return None


def kelola_akun(akun_login):
    while True:
        daftar_akun = baca_data(file_akun)
        print("\n=====KELOLA AKUN=====")
        print("1. Lihat akun")
        print("2. Tambah akun")
        print("3. Ubah role akun")
        print("4. Hapus akun")
        print("5. Kembali")
        pilihan = input_angka("Pilihan: ")

        if pilihan == 1:
            tampilkan_akun(daftar_akun)

        elif pilihan == 2:
            username = input_teks("Username baru: ")
            if cari_akun(daftar_akun, username):
                print("Username sudah dipakai")
                continue
            password = input_teks("Password: ")
            role = input_teks("Role (admin/petugas/user): ").lower()
            if role not in ROLE_VALID:
                print("Role tidak valid")
                continue
            daftar_akun.append({"username": username, "password": password, "role": role})
            simpan_data(file_akun, daftar_akun)
            print("Akun berhasil ditambahkan")

        elif pilihan == 3:
            tampilkan_akun(daftar_akun)
            username = input_teks("Username yang diubah: ")
            akun = cari_akun(daftar_akun, username)
            if akun is None:
                print("Akun tidak ditemukan")
                continue
            if username == akun_login["username"]:
                print("Anda tidak bisa mengubah role akun sendiri")
                continue
            role = input_teks("Role baru (admin/petugas/user): ").lower()
            if role not in ROLE_VALID:
                print("Role tidak valid")
                continue
            akun["role"] = role
            simpan_data(file_akun, daftar_akun)
            print("Role berhasil diubah")

        elif pilihan == 4:
            tampilkan_akun(daftar_akun)
            username = input_teks("Username yang dihapus: ")
            akun = cari_akun(daftar_akun, username)
            if akun is None:
                print("Akun tidak ditemukan")
                continue
            if username == akun_login["username"]:
                print("Anda tidak bisa menghapus akun sendiri")
                continue
            if konfirmasi(f"Yakin hapus akun {username}?"):
                daftar_akun.remove(akun)
                simpan_data(file_akun, daftar_akun)
                print("Akun berhasil dihapus")

        elif pilihan == 5:
            return
        else:
            print("Pilihan tidak valid")


# =====================================================
# 2. KELOLA INFORMASI KONSER
# =====================================================
FIELD_KONSER = {
    1: ("judul", "Judul"),
    2: ("tanggal", "Tanggal"),
    3: ("waktu", "Waktu"),
    4: ("lokasi", "Lokasi"),
}


def kelola_informasi_konser():
    while True:
        konser = baca_data(file_konser)
        print("\n=====KELOLA INFORMASI KONSER=====")
        for key, label in FIELD_KONSER.values():
            print(f"{label:<8}: {konser.get(key, '-')}")
        print("\n1. Ubah judul")
        print("2. Ubah tanggal")
        print("3. Ubah waktu")
        print("4. Ubah lokasi")
        print("5. Kembali")
        pilihan = input_angka("Pilihan: ")

        if pilihan in FIELD_KONSER:
            key, label = FIELD_KONSER[pilihan]
            konser[key] = input_teks(f"{label} baru: ")
            simpan_data(file_konser, konser)
            print(f"{label} berhasil diubah")
        elif pilihan == 5:
            return
        else:
            print("Pilihan tidak valid")


# =====================================================
# 3. KELOLA KATALOG TIKET
# =====================================================
def tampilkan_katalog(konser):
    print("\n=====KATALOG TIKET=====")
    kategori_list = konser.get("kategori", [])
    if not kategori_list:
        print("Belum ada kategori tiket")
        return
    for k in kategori_list:
        print(f"{k['nomor']}. {k['jenis']} - {rupiah(int(k['harga']))} (kuota: {k['kuota']})")


def kelola_katalog():
    while True:
        konser = baca_data(file_konser)
        daftar_tiket = baca_data(file_tiket)
        kategori_list = konser.setdefault("kategori", [])

        print("\n=====KELOLA KATALOG TIKET=====")
        print("1. Lihat katalog")
        print("2. Tambah kategori")
        print("3. Ubah kategori")
        print("4. Hapus kategori")
        print("5. Kembali")
        pilihan = input_angka("Pilihan: ")

        if pilihan == 1:
            tampilkan_katalog(konser)

        elif pilihan == 2:
            jenis = input_teks("Nama kategori: ")
            if any(k["jenis"].lower() == jenis.lower() for k in kategori_list):
                print("Kategori sudah ada")
                continue
            harga = baca_angka("Harga per tiket: ")
            kuota = baca_angka("Kuota: ")
            if harga is None or kuota is None or harga < 1 or kuota < 1:
                print("Harga dan kuota harus angka lebih dari 0")
                continue
            nomor = max([k["nomor"] for k in kategori_list], default=0) + 1
            kategori_list.append({"nomor": nomor, "jenis": jenis, "harga": harga, "kuota": kuota})
            simpan_data(file_konser, konser)
            print("Kategori berhasil ditambahkan")

        elif pilihan == 3:
            tampilkan_katalog(konser)
            nomor = input_angka("Nomor kategori yang diubah: ")
            kategori = cari_kategori_nomor(konser, nomor)
            if kategori is None:
                print("Kategori tidak ditemukan")
                continue
            print("1. Ubah harga")
            print("2. Ubah kuota")
            print("3. Ubah nama")
            sub = input_angka("Pilihan: ")
            if sub == 1:
                harga = baca_angka("Harga baru: ")
                if harga is None or harga < 1:
                    print("Harga harus lebih dari 0")
                    continue
                kategori["harga"] = harga
            elif sub == 2:
                kuota = baca_angka("Kuota baru: ")
                if kuota is None or kuota < 0:
                    print("Kuota tidak valid")
                    continue
                kategori["kuota"] = kuota
            elif sub == 3:
                if any(p["kategori"] == kategori["jenis"] for p in daftar_tiket):
                    print("Nama tidak bisa diubah karena sudah ada pesanan untuk kategori ini")
                    continue
                kategori["jenis"] = input_teks("Nama baru: ")
            else:
                print("Pilihan tidak valid")
                continue
            simpan_data(file_konser, konser)
            print("Kategori berhasil diubah")

        elif pilihan == 4:
            tampilkan_katalog(konser)
            nomor = input_angka("Nomor kategori yang dihapus: ")
            kategori = cari_kategori_nomor(konser, nomor)
            if kategori is None:
                print("Kategori tidak ditemukan")
                continue
            if any(p["kategori"] == kategori["jenis"] and p["status"] in STATUS_AKTIF
                   for p in daftar_tiket):
                print("Tidak bisa dihapus, masih ada pesanan aktif di kategori ini")
                continue
            if konfirmasi(f"Yakin hapus kategori {kategori['jenis']}?"):
                kategori_list.remove(kategori)
                simpan_data(file_konser, konser)
                print("Kategori berhasil dihapus")

        elif pilihan == 5:
            return
        else:
            print("Pilihan tidak valid")


# =====================================================
# 4. KELOLA KETENTUAN DISKON
# =====================================================
def tampilkan_aturan_diskon(aturan):
    print("\n=====KETENTUAN DISKON=====")
    if not aturan:
        print("Belum ada ketentuan diskon")
        return
    for i, a in enumerate(aturan, 1):
        if a["min_tiket"] == a["maks_tiket"]:
            rentang = f"{a['min_tiket']} tiket"
        else:
            rentang = f"{a['min_tiket']}-{a['maks_tiket']} tiket"
        print(f"{i}. Beli {rentang}: diskon {a['persen']}%")


def kelola_diskon():
    while True:
        konser = baca_data(file_konser)
        aturan = ambil_aturan_diskon(konser)

        print("\n=====KELOLA KETENTUAN DISKON=====")
        print("1. Lihat ketentuan")
        print("2. Tambah ketentuan")
        print("3. Ubah persen diskon")
        print("4. Hapus ketentuan")
        print("5. Kembali")
        pilihan = input_angka("Pilihan: ")

        if pilihan == 1:
            tampilkan_aturan_diskon(aturan)

        elif pilihan == 2:
            print(f"(Pembelian maksimal {MAKS_TIKET} tiket per pesanan)")
            minimal = baca_angka("Jumlah tiket minimal: ")
            maksimal = baca_angka("Jumlah tiket maksimal: ")
            persen = baca_angka("Persen diskon (1-100): ")
            if None in (minimal, maksimal, persen):
                continue
            if not (1 <= minimal <= maksimal <= MAKS_TIKET):
                print(f"Rentang tidak valid (1 sampai {MAKS_TIKET}, minimal tidak boleh lebih besar dari maksimal)")
                continue
            if not (1 <= persen <= 100):
                print("Persen harus 1 sampai 100")
                continue
            if any(a["min_tiket"] <= maksimal and minimal <= a["maks_tiket"] for a in aturan):
                print("Rentang bertabrakan dengan ketentuan yang sudah ada")
                continue
            aturan.append({"min_tiket": minimal, "maks_tiket": maksimal, "persen": persen})
            aturan.sort(key=lambda a: a["min_tiket"])
            konser["diskon"] = aturan
            simpan_data(file_konser, konser)
            print("Ketentuan diskon berhasil ditambahkan")

        elif pilihan == 3:
            tampilkan_aturan_diskon(aturan)
            no = input_angka("Nomor ketentuan yang diubah: ")
            if not (1 <= no <= len(aturan)):
                print("Nomor tidak valid")
                continue
            persen = baca_angka("Persen diskon baru (0-100): ")
            if persen is None or not (0 <= persen <= 100):
                print("Persen harus 0 sampai 100")
                continue
            aturan[no - 1]["persen"] = persen
            konser["diskon"] = aturan
            simpan_data(file_konser, konser)
            print("Persen diskon berhasil diubah")

        elif pilihan == 4:
            tampilkan_aturan_diskon(aturan)
            no = input_angka("Nomor ketentuan yang dihapus: ")
            if not (1 <= no <= len(aturan)):
                print("Nomor tidak valid")
                continue
            if konfirmasi("Yakin hapus ketentuan ini?"):
                aturan.pop(no - 1)
                konser["diskon"] = aturan
                simpan_data(file_konser, konser)
                print("Ketentuan diskon berhasil dihapus")

        elif pilihan == 5:
            return
        else:
            print("Pilihan tidak valid")


# =====================================================
# 5. LIHAT SELURUH TRANSAKSI PEMESANAN
# =====================================================
def lihat_transaksi_pemesanan():
    daftar_tiket = baca_data(file_tiket)
    print("\n=====TRANSAKSI PEMESANAN=====")
    if not daftar_tiket:
        print("Belum ada transaksi")
        return

    print("Filter status:")
    print("1. Semua")
    print("2. Menunggu Pembayaran")
    print("3. Lunas")
    print("4. Dibatalkan")
    pilihan = input_angka("Pilihan: ")
    filter_status = {2: "Menunggu Pembayaran", 3: "Lunas", 4: "Dibatalkan"}.get(pilihan)

    if filter_status:
        daftar = [p for p in daftar_tiket if p["status"] == filter_status]
    else:
        daftar = daftar_tiket

    if not daftar:
        print("Tidak ada transaksi dengan status tersebut")
        return
    print()
    tampilkan_tabel_pesanan(daftar)
    print(f"\nTotal transaksi: {len(daftar)}")


# =====================================================
# 6. KELOLA DAN VERIFIKASI PEMBAYARAN
# =====================================================
def kelola_verifikasi_pembayaran():
    daftar_tiket = baca_data(file_tiket)
    konser = baca_data(file_konser)
    menunggu = [p for p in daftar_tiket if p["status"] == "Menunggu Pembayaran"]

    print("\n=====VERIFIKASI PEMBAYARAN=====")
    if not menunggu:
        print("Tidak ada pembayaran yang menunggu verifikasi")
        return

    tampilkan_tabel_pesanan(menunggu)
    kode = input("\nKode pesan (kosongkan untuk kembali): ").strip()
    if kode == "":
        return
    pesanan = cari_pesanan(menunggu, kode)
    if pesanan is None:
        print("Kode pesan tidak ditemukan")
        return

    print("1. Verifikasi (jadikan Lunas)")
    print("2. Tolak (jadikan Dibatalkan)")
    pilihan = input_angka("Pilihan: ")

    if pilihan == 1:
        kategori = cari_kategori(konser, pesanan["kategori"])
        if kategori is None:
            print("Kategori pesanan sudah tidak ada di katalog")
            return
        if kategori["kuota"] < pesanan["jumlah"]:
            print("Kuota tidak mencukupi, pembayaran tidak bisa diverifikasi")
            return
        kategori["kuota"] -= pesanan["jumlah"]
        pesanan["status"] = "Lunas"
        if not pesanan.get("kode_unik"):
            pesanan["kode_unik"] = buat_kode_unik()
        simpan_data(file_konser, konser)
        simpan_data(file_tiket, daftar_tiket)
        print("Pembayaran terverifikasi, status: Lunas")

    elif pilihan == 2:
        if konfirmasi("Yakin tolak pembayaran ini?"):
            pesanan["status"] = "Dibatalkan"
            simpan_data(file_tiket, daftar_tiket)
            print("Pembayaran ditolak, pesanan dibatalkan")
    else:
        print("Pilihan tidak valid")


# =====================================================
# 7. KELOLA PEMBATALAN TIKET
# =====================================================
def kelola_pembatalan_tiket():
    daftar_tiket = baca_data(file_tiket)
    konser = baca_data(file_konser)
    aktif = [p for p in daftar_tiket if p["status"] in STATUS_AKTIF]

    print("\n=====PEMBATALAN TIKET=====")
    if not aktif:
        print("Tidak ada pesanan yang bisa dibatalkan")
        return

    tampilkan_tabel_pesanan(aktif)
    kode = input("\nKode pesan yang dibatalkan (kosongkan untuk kembali): ").strip()
    if kode == "":
        return
    pesanan = cari_pesanan(aktif, kode)
    if pesanan is None:
        print("Kode pesan tidak ditemukan")
        return

    if not konfirmasi(f"Yakin batalkan pesanan {pesanan['kode_pesan']}?"):
        return

    # kuota baru terpotong saat pesanan Lunas, jadi hanya pesanan Lunas yang mengembalikan kuota
    if pesanan["status"] == "Lunas":
        kategori = cari_kategori(konser, pesanan["kategori"])
        if kategori is not None:
            kategori["kuota"] += pesanan["jumlah"]
            simpan_data(file_konser, konser)

    pesanan["status"] = "Dibatalkan"
    simpan_data(file_tiket, daftar_tiket)
    print("Pesanan berhasil dibatalkan")


# =====================================================
# 8. LIHAT LAPORAN PENJUALAN TIKET
# =====================================================
def lihat_laporan_penjualan():
    daftar_tiket = baca_data(file_tiket)
    print("\n=====LAPORAN PENJUALAN TIKET=====")
    if not daftar_tiket:
        print("Belum ada transaksi")
        return

    lunas = [p for p in daftar_tiket if p["status"] == "Lunas"]
    menunggu = [p for p in daftar_tiket if p["status"] == "Menunggu Pembayaran"]
    batal = [p for p in daftar_tiket if p["status"] == "Dibatalkan"]

    total_tiket = sum(p["jumlah"] for p in lunas)
    total_diskon = sum(p["diskon"] for p in lunas)
    total_pendapatan = sum(p["total_bayar"] for p in lunas)

    print("Transaksi lunas       :", len(lunas))
    print("Menunggu pembayaran   :", len(menunggu))
    print("Dibatalkan            :", len(batal))
    print("Total tiket terjual   :", total_tiket)
    print("Total diskon diberikan:", rupiah(total_diskon))
    print("Total pendapatan      :", rupiah(total_pendapatan))

    per_kategori = {}
    for p in lunas:
        data = per_kategori.setdefault(p["kategori"], {"tiket": 0, "pendapatan": 0})
        data["tiket"] += p["jumlah"]
        data["pendapatan"] += p["total_bayar"]

    if per_kategori:
        print("\nRincian per kategori:")
        print(f"{'Kategori':<12}{'Tiket':<8}{'Pendapatan':<15}")
        print("-" * 35)
        for jenis, data in per_kategori.items():
            print(f"{jenis:<12}{data['tiket']:<8}{rupiah(data['pendapatan']):<15}")


# =====================================================
# MENU ADMIN
# =====================================================
def menu_admin(akun):
    while True:
        print("\n=====MENU ADMIN=====")
        print("1. Kelola akun")
        print("2. Kelola informasi konser")
        print("3. Kelola katalog")
        print("4. Kelola ketentuan diskon pembelian tiket")
        print("5. Lihat seluruh transaksi pemesanan")
        print("6. Kelola dan verifikasi pembayaran")
        print("7. Kelola pembatalan tiket")
        print("8. Lihat laporan penjualan tiket")
        print("9. Logout")

        menu = input_angka("Input menu: ")

        if menu == 1:
            kelola_akun(akun)
        elif menu == 2:
            kelola_informasi_konser()
        elif menu == 3:
            kelola_katalog()
        elif menu == 4:
            kelola_diskon()
        elif menu == 5:
            lihat_transaksi_pemesanan()
        elif menu == 6:
            kelola_verifikasi_pembayaran()
        elif menu == 7:
            kelola_pembatalan_tiket()
        elif menu == 8:
            lihat_laporan_penjualan()
        elif menu == 9:
            print("Logout berhasil")
            break
        else:
            print("Menu tidak valid")