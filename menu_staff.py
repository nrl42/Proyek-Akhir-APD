from database import baca_data, simpan_data
from bantuan import rupiah

FILE_AKUN = "data/akun_user.json"
FILE_TIKET = "data/tiket.json"
FILE_KONSER = "data/konser.json"
FILE_DISKON = "data/diskon.json"


DISKON_DEFAULT = [
    {"min": 2, "max": 2, "persen": 5},
    {"min": 3, "max": 4, "persen": 10},
]

ROLE_VALID = ["admin", "petugas", "user"]


def _baca(path, default):
    try:
        data = baca_data(path)
    except Exception:
        return default
    return data if isinstance(data, type(default)) else default


def _input_angka(pesan, minimum=None):
    while True:
        try:
            nilai = int(input(pesan).strip())
            if minimum is not None and nilai < minimum:
                print(f"Nilai minimal {minimum}.")
                continue
            return nilai
        except ValueError:
            print("Input harus berupa angka.")


def _nama_user(user):
    return user.get("username", "-") if isinstance(user, dict) else str(user)


def _id_baru(daftar):
    ids = [d.get("id", 0) for d in daftar if isinstance(d.get("id", 0), int)]
    return (max(ids) + 1) if ids else 1


def _daftar_diskon():
    data = _baca(FILE_DISKON, [])
    return data if data else DISKON_DEFAULT


def _persen_diskon(jumlah):
    for aturan in _daftar_diskon():
        if aturan["min"] <= jumlah <= aturan["max"]:
            return aturan["persen"]
    return 


def _subtotal(t):
    if "subtotal" in t:
        return t["subtotal"]
    return t.get("harga", 0) * t.get("jumlah", 0)


def _kembalikan_kuota(pesanan):
    """Kembalikan kuota tiket ke konser saat pesanan dibatalkan."""
    konser_list = _baca(FILE_KONSER, [])
    for k in konser_list:
        if k.get("id") == pesanan.get("id_konser"):
            for kat in k.get("kategori", []):
                if kat.get("nomor") == pesanan.get("nomor_kategori"):
                    kat["kuota"] = kat.get("kuota", 0) + pesanan.get("jumlah", 0)
                    simpan_data(FILE_KONSER, konser_list)
                    return


def _cetak_pesanan(i, t):
    print(f"{i}. ID: {t.get('id')} | Pemesan: {t.get('username')} | "
          f"Konser: {t.get('konser', '-')} | Kategori: {t.get('kategori', '-')} | "
          f"Jumlah: {t.get('jumlah', 0)} | Total: {rupiah(t.get('total', 0))} | "
          f"Status: {t.get('status', '-')}")


def kelola_akun(user_login):
    while True:
        akun = _baca(FILE_AKUN, [])
        print("\n=== KELOLA AKUN ===")
        print("1. Lihat semua akun")
        print("2. Tambah akun")
        print("3. Ubah role akun")
        print("4. Hapus akun")
        print("5. Kembali")
        pilih = input("Pilih: ").strip()

        if pilih == "1":
            if not akun:
                print("Belum ada akun.")
            for i, a in enumerate(akun, 1):
                print(f"{i}. {a.get('username')} | role: {a.get('role')}")

        elif pilih == "2":
            username = input("Username baru: ").strip()
            if not username:
                print("Username tidak boleh kosong.")
                continue
            if any(a.get("username") == username for a in akun):
                print("Username sudah dipakai.")
                continue
            password = input("Password: ").strip()
            role = input(f"Role {ROLE_VALID}: ").strip().lower()
            if role not in ROLE_VALID:
                print("Role tidak valid.")
                continue
            akun.append({"username": username, "password": password, "role": role})
            simpan_data(FILE_AKUN, akun)
            print("Akun berhasil ditambahkan.")

        elif pilih == "3":
            username = input("Username yang diubah: ").strip()
            target = next((a for a in akun if a.get("username") == username), None)
            if not target:
                print("Akun tidak ditemukan.")
                continue
            role = input(f"Role baru {ROLE_VALID}: ").strip().lower()
            if role not in ROLE_VALID:
                print("Role tidak valid.")
                continue
            target["role"] = role
            simpan_data(FILE_AKUN, akun)
            print("Role berhasil diubah.")

        elif pilih == "4":
            username = input("Username yang dihapus: ").strip()
            if username == _nama_user(user_login):
                print("Tidak bisa menghapus akun yang sedang dipakai.")
                continue
            target = next((a for a in akun if a.get("username") == username), None)
            if not target:
                print("Akun tidak ditemukan.")
                continue
            yakin = input(f"Yakin hapus '{username}'? (y/n): ").strip().lower()
            if yakin == "y":
                akun.remove(target)
                simpan_data(FILE_AKUN, akun)
                print("Akun berhasil dihapus.")

        elif pilih == "5":
            return
        else:
            print("Pilihan tidak valid.")


def _tampil_konser(konser_list):
    if not konser_list:
        print("Belum ada konser.")
        return
    for k in konser_list:
        print(f"\n[{k.get('id')}] {k.get('nama')} | {k.get('tanggal')} | {k.get('lokasi')}")
        for kat in k.get("kategori", []):
            print(f"    {kat.get('nomor')}. {kat.get('jenis')} - "
                  f"{rupiah(kat.get('harga', 0))} - kuota {kat.get('kuota', 0)}")


def _cari_konser(konser_list):
    id_konser = _input_angka("ID konser: ")
    return next((k for k in konser_list if k.get("id") == id_konser), None)


def kelola_konser():
    while True:
        konser_list = _baca(FILE_KONSER, [])
        print("\n=== KELOLA KONSER DAN KATALOG TIKET ===")
        print("1. Lihat konser dan katalog tiket")
        print("2. Tambah konser")
        print("3. Ubah data konser")
        print("4. Hapus konser")
        print("5. Tambah kategori tiket")
        print("6. Ubah harga / kuota kategori")
        print("7. Hapus kategori tiket")
        print("8. Kembali")
        pilih = input("Pilih: ").strip()

        if pilih == "1":
            _tampil_konser(konser_list)

        elif pilih == "2":
            nama = input("Nama konser: ").strip()
            tanggal = input("Tanggal: ").strip()
            lokasi = input("Lokasi: ").strip()
            if not nama:
                print("Nama konser tidak boleh kosong.")
                continue
            konser_list.append({"id": _id_baru(konser_list), "nama": nama,
                                "tanggal": tanggal, "lokasi": lokasi, "kategori": []})
            simpan_data(FILE_KONSER, konser_list)
            print("Konser berhasil ditambahkan. Tambahkan kategori tiketnya (menu 5).")

        elif pilih == "3":
            _tampil_konser(konser_list)
            k = _cari_konser(konser_list)
            if not k:
                print("Konser tidak ditemukan.")
                continue
            k["nama"] = input(f"Nama [{k.get('nama')}]: ").strip() or k.get("nama")
            k["tanggal"] = input(f"Tanggal [{k.get('tanggal')}]: ").strip() or k.get("tanggal")
            k["lokasi"] = input(f"Lokasi [{k.get('lokasi')}]: ").strip() or k.get("lokasi")
            simpan_data(FILE_KONSER, konser_list)
            print("Data konser diperbarui.")

        elif pilih == "4":
            _tampil_konser(konser_list)
            k = _cari_konser(konser_list)
            if not k:
                print("Konser tidak ditemukan.")
                continue
            if input(f"Yakin hapus '{k.get('nama')}'? (y/n): ").strip().lower() == "y":
                konser_list.remove(k)
                simpan_data(FILE_KONSER, konser_list)
                print("Konser dihapus.")

        elif pilih == "5":
            _tampil_konser(konser_list)
            k = _cari_konser(konser_list)
            if not k:
                print("Konser tidak ditemukan.")
                continue
            kategori = k.setdefault("kategori", [])
            jenis = input("Jenis tiket (mis. VIP, Festival): ").strip()
            harga = _input_angka("Harga: ", 0)
            kuota = _input_angka("Kuota: ", 0)
            nomor = (max([c.get("nomor", 0) for c in kategori]) + 1) if kategori else 1
            kategori.append({"nomor": nomor, "jenis": jenis, "harga": harga, "kuota": kuota})
            simpan_data(FILE_KONSER, konser_list)
            print("Kategori tiket ditambahkan.")

        elif pilih in ("6", "7"):
            _tampil_konser(konser_list)
            k = _cari_konser(konser_list)
            if not k:
                print("Konser tidak ditemukan.")
                continue
            nomor = _input_angka("Nomor kategori: ")
            kat = next((c for c in k.get("kategori", []) if c.get("nomor") == nomor), None)
            if not kat:
                print("Kategori tidak ditemukan.")
                continue
            if pilih == "6":
                kat["harga"] = _input_angka(f"Harga baru [{kat.get('harga')}]: ", 0)
                kat["kuota"] = _input_angka(f"Kuota baru [{kat.get('kuota')}]: ", 0)
                print("Kategori diperbarui.")
            else:
                k["kategori"].remove(kat)
                print("Kategori dihapus.")
            simpan_data(FILE_KONSER, konser_list)

        elif pilih == "8":
            return
        else:
            print("Pilihan tidak valid.")


def kelola_diskon():
    while True:
        aturan = _daftar_diskon()
        print("\n=== KELOLA KETENTUAN DISKON ===")
        for i, a in enumerate(aturan, 1):
            print(f"{i}. {a['min']}-{a['max']} tiket = {a['persen']}%")
        print("\n1. Ubah persen diskon")
        print("2. Tambah aturan")
        print("3. Hapus aturan")
        print("4. Kembali")
        pilih = input("Pilih: ").strip()

        if pilih == "1":
            no = _input_angka("Nomor aturan: ", 1)
            if no > len(aturan):
                print("Nomor tidak ada.")
                continue
            persen = _input_angka("Persen baru (0-100): ", 0)
            if persen > 100:
                print("Persen maksimal 100.")
                continue
            aturan[no - 1]["persen"] = persen
            simpan_data(FILE_DISKON, aturan)
            print("Diskon diperbarui.")

        elif pilih == "2":
            minimum = _input_angka("Jumlah tiket minimum: ", 1)
            maksimum = _input_angka("Jumlah tiket maksimum: ", minimum)
            persen = _input_angka("Persen diskon (0-100): ", 0)
            if persen > 100:
                print("Persen maksimal 100.")
                continue
            aturan.append({"min": minimum, "max": maksimum, "persen": persen})
            simpan_data(FILE_DISKON, aturan)
            print("Aturan ditambahkan.")

        elif pilih == "3":
            no = _input_angka("Nomor aturan: ", 1)
            if no > len(aturan):
                print("Nomor tidak ada.")
                continue
            aturan.pop(no - 1)
            simpan_data(FILE_DISKON, aturan)
            print("Aturan dihapus.")

        elif pilih == "4":
            return
        else:
            print("Pilihan tidak valid.")


def lihat_transaksi():
    data = _baca(FILE_TIKET, [])
    print("\n=== SELURUH TRANSAKSI PEMESANAN ===")
    if not data:
        print("Belum ada transaksi.")
        return
    for i, t in enumerate(data, 1):
        _cetak_pesanan(i, t)
    print(f"\nTotal transaksi: {len(data)}")


def verifikasi_pembayaran():
    while True:
        data = _baca(FILE_TIKET, [])
        menunggu = [t for t in data if t.get("status") == "Menunggu Pembayaran"]

        print("\n=== KELOLA DAN VERIFIKASI PEMBAYARAN ===")
        if not menunggu:
            print("Tidak ada pembayaran yang perlu diverifikasi.")
            return

        for i, t in enumerate(menunggu, 1):
            _cetak_pesanan(i, t)
        print("0. Kembali")

        pilih = input("Pilih pesanan yang akan diverifikasi: ").strip()
        if pilih == "0":
            return
        if not pilih.isdigit() or not (1 <= int(pilih) <= len(menunggu)):
            print("Pilihan tidak valid.")
            continue

        terpilih = menunggu[int(pilih) - 1]
        print("\n1. Verifikasi (ubah ke Lunas)")
        print("2. Tolak (ubah ke Dibatalkan)")
        print("3. Batal")
        aksi = input("Pilih aksi: ").strip()

        if aksi == "1":
            terpilih["status"] = "Lunas"
            print("Pembayaran berhasil diverifikasi.")
        elif aksi == "2":
            terpilih["status"] = "Dibatalkan"
            _kembalikan_kuota(terpilih)
            print("Pembayaran ditolak, pesanan dibatalkan.")
        else:
            print("Dibatalkan.")
            continue

        simpan_data(FILE_TIKET, data)


def kelola_pembatalan():
    while True:
        data = _baca(FILE_TIKET, [])
        aktif = [t for t in data if t.get("status") != "Dibatalkan"]

        print("\n=== KELOLA PEMBATALAN TIKET ===")
        if not aktif:
            print("Tidak ada pesanan yang bisa dibatalkan.")
            return

        for i, t in enumerate(aktif, 1):
            _cetak_pesanan(i, t)
        print("0. Kembali")

        pilih = input("Pilih pesanan: ").strip()
        if pilih == "0":
            return
        if not pilih.isdigit() or not (1 <= int(pilih) <= len(aktif)):
            print("Pilihan tidak valid.")
            continue

        t = aktif[int(pilih) - 1]
        if t.get("status") == "Pengajuan Pembatalan":
            print("\n1. Setujui pembatalan")
            print("2. Tolak pembatalan")
            print("3. Batal")
            aksi = input("Pilih aksi: ").strip()
            if aksi == "1":
                t["status"] = "Dibatalkan"
                _kembalikan_kuota(t)
                print("Pembatalan disetujui, kuota dikembalikan.")
            elif aksi == "2":
                t["status"] = t.get("status_sebelum", "Lunas")
                print("Pengajuan pembatalan ditolak.")
            else:
                continue
        else:
            if input("Batalkan pesanan ini? (y/n): ").strip().lower() != "y":
                continue
            t["status"] = "Dibatalkan"
            _kembalikan_kuota(t)
            print("Pesanan dibatalkan, kuota dikembalikan.")

        simpan_data(FILE_TIKET, data)


def lihat_rincian_harga():
    data = _baca(FILE_TIKET, [])
    print("\n=== RINCIAN HARGA SEBELUM DAN SESUDAH DISKON ===")
    data = [t for t in data if t.get("status") != "Dibatalkan"]
    if not data:
        print("Belum ada transaksi.")
        return

    for t in data:
        sub = _subtotal(t)
        persen = t.get("diskon_persen", _persen_diskon(t.get("jumlah", 0)))
        potongan = sub * persen // 100
        total = t.get("total", sub - potongan)
        print(f"\nID {t.get('id')} | {t.get('username')} | {t.get('konser', '-')} "
              f"({t.get('kategori', '-')}) x {t.get('jumlah', 0)}")
        print(f"  Harga sebelum diskon : {rupiah(sub)}")
        print(f"  Diskon ({persen}%)       : {rupiah(potongan)}")
        print(f"  Harga sesudah diskon : {rupiah(total)}")


def laporan_penjualan():
    data = _baca(FILE_TIKET, [])
    lunas = [t for t in data if t.get("status") == "Lunas"]

    print("\n=== LAPORAN PENJUALAN TIKET (TRANSAKSI LUNAS) ===")
    if not lunas:
        print("Belum ada penjualan berstatus Lunas.")
        return

    per_konser = {}
    pendapatan = 0
    for t in lunas:
        nama = t.get("konser", "-")
        per_konser[nama] = per_konser.get(nama, 0) + t.get("jumlah", 0)
        pendapatan += t.get("total", 0)

    terbanyak = max(per_konser.values())
    skala = 40 / terbanyak if terbanyak > 40 else 1
    lebar_nama = max(len(n) for n in per_konser)

    for nama, jumlah in per_konser.items():
        bar = "#" * max(1, int(jumlah * skala))
        print(f"{nama:<{lebar_nama}} | {bar} {jumlah}")

    print(f"\nTotal tiket terjual : {sum(per_konser.values())}")
    print(f"Total pendapatan    : {rupiah(pendapatan)}")


def menu_admin(user):
    while True:
        print("\n=== MENU ADMIN ===")
        print(f"Selamat datang, {_nama_user(user)}")
        print("1. Kelola akun")
        print("2. Kelola informasi konser dan katalog tiket")
        print("3. Kelola ketentuan diskon pembelian tiket")
        print("4. Lihat seluruh transaksi pemesanan")
        print("5. Kelola dan verifikasi pembayaran")
        print("6. Kelola pembatalan tiket")
        print("7. Lihat rincian harga sebelum dan sesudah diskon")
        print("8. Lihat laporan penjualan tiket (diagram batang)")
        print("9. Logout")
        pilihan = input("Input menu: ").strip()

        if pilihan == "1":
            kelola_akun(user)
        elif pilihan == "2":
            kelola_konser()
        elif pilihan == "3":
            kelola_diskon()
        elif pilihan == "4":
            lihat_transaksi()
        elif pilihan == "5":
            verifikasi_pembayaran()
        elif pilihan == "6":
            kelola_pembatalan()
        elif pilihan == "7":
            lihat_rincian_harga()
        elif pilihan == "8":
            laporan_penjualan()
        elif pilihan == "9":
            print("Logout berhasil.")
            break
        else:
            print("Pilihan tidak valid.")


def menu_petugas(user):
    while True:
        print("\n=== MENU PETUGAS ===")
        print(f"Selamat datang, {_nama_user(user)}")
        print("1. Lihat seluruh transaksi pemesanan")
        print("2. Kelola dan verifikasi pembayaran")
        print("3. Kelola pembatalan tiket")
        print("4. Lihat rincian harga sebelum dan sesudah diskon")
        print("5. Lihat laporan penjualan tiket (diagram batang)")
        print("6. Logout")
        pilihan = input("Input menu: ").strip()

        if pilihan == "1":
            lihat_transaksi()
        elif pilihan == "2":
            verifikasi_pembayaran()
        elif pilihan == "3":
            kelola_pembatalan()
        elif pilihan == "4":
            lihat_rincian_harga()
        elif pilihan == "5":
            laporan_penjualan()
        elif pilihan == "6":
            print("Logout berhasil.")
            break
        else:
            print("Pilihan tidak valid.")