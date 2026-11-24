# from database import baca_data, simpan_data, file_tiket, file_konser, file_diskon
# from bantuan import rupiah, buat_kode_unik

# def hitung_diskon(jumlah, harga_awal):
#     daftar_diskon = baca_data(file_diskon)
#     persen = 0
#     for d in daftar_diskon:
#         if d["min_tiket"] <= jumlah <= d["maks_tiket"] and d["persen"] > persen:
#             persen = d["persen"]
#     return harga_awal * persen // 100

# def cari_pesanan(daftar_tiket, kode_pesan):
#     for tiket in daftar_tiket:
#         if tiket ["kode_pesanan"] == kode_pesanan:
#             return tiket
#     return None

# def kembalikan_kuota(pesanan):
#     konser = baca_data(file_konser)
#     for k in konser ["kategori"]:
#         if k["nomor"] == pesanan["nomor_kategori"]:
#             k["kuota"] = k["kuota"] + pesanan["jumlah"]
#             simpan_data(file_konser, konser)

# def aktifkan_tiket(pesanan, daftar_tiket):
#     while True:
#         kode = buat_kode_unik()
#         bentrok = False
#         for tiket in daftar_tiket:
#             if tiket["kode_unik"] == kode:
#                 bentrok = True
#         if not bentrok:
#             break
#     pesanan["kode_unik"] = kode
#     pesanan["status_tiket"] = "Active"

# def tampilkan_daftar_transaksi(daftar_tiket):
#     print("\n=====DAFTAR TRANSAKSI=====")
#     for t in daftar_tiket:
#         print(f"{t['kode_pesan']} | {t['username']} | {t['kategori']} x {t['jumlah']} | " f"{rupiah(t['total_bayar'])} | {t['status']}")

# def tampilkan_detail_pesanan(t):
#     print("\n-----------------------------")
#     print("Kode pesan   :", t["kode_pesan"])
#     print("Pelanggan    :", t["username"])
#     print("Kategori     :", t["kategori"])
#     print("Jumlah       :", t["jumlah"])
#     print("Total bayar  :", rupiah(t["total_bayar"]))
#     print("Kode unik    :", t["kode_unik"] if t["kode_unik"] != "" else "-")
#     print("Status       :", t["status"])
#     print("Status tiket :", t["status_tiket"])
#     print("-----------------------------")


# def lihat_rincian_harga():
#     daftar_tiket = baca_data(file_tiket)
#     print("\n=====RINCIAN HARGA SEBELUM & SESUDAH DISKON=====")

#     if len(daftar_tiket) == 0:
#         print("Belum ada data pemesanan.")
#         return

#     tampilkan_daftar_transaksi(daftar_tiket)
#     kode = input("\nMasukkan kode pesan: ").strip().upper()
#     pesanan = cari_pesanan(daftar_tiket, kode)

#     if pesanan is None:
#         print("Kode pemesanan tidak ditemukan.")
#         return

#     persen = 0
#     if pesanan["harga_awal"] > 0:
#         persen = pesanan["diskon"] * 100 // pesanan["harga_awal"]

#     print("\n=====RINCIAN HARGA=====")
#     print("Kategori        :", pesanan["kategori"])
#     print("Harga per tiket :", rupiah(pesanan["harga_awal"] // pesanan["jumlah"]))
#     print("Jumlah tiket    :", pesanan["jumlah"])
#     print("Harga awal      :", rupiah(pesanan["harga_awal"]))
#     print(f"Diskon ({persen}%)    :", rupiah(pesanan["diskon"]))
#     print("Total bayar     :", rupiah(pesanan["total_bayar"]))