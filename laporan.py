import os

from bantuan import gagal, info, peringatan, rupiah, tabel, waktu_sekarang
from database import baca_data, file_konser, file_tiket, folder_data

file_grafik = os.path.join(folder_data, "grafik_penjualan.png")
file_laporan = os.path.join(folder_data, "laporan_penjualan.txt")

STATUS_TERJUAL = ("Lunas",)


def hitung_penjualan():
    konser = baca_data(file_konser)
    hasil = {k["jenis"]: (0, 0) for k in konser["kategori"]}
    pembeli = set()

    for t in baca_data(file_tiket):
        if t["status"] in STATUS_TERJUAL and t["kategori"] in hasil:
            terjual, pendapatan = hasil[t["kategori"]]
            hasil[t["kategori"]] = (terjual + t["jumlah"], pendapatan + t["total_bayar"])
            pembeli.add(t["username"])
    return hasil, pembeli


def hitung_total(hasil):
    total_tiket = sum(terjual for terjual, _ in hasil.values())
    total_uang = sum(pendapatan for _, pendapatan in hasil.values())
    return total_tiket, total_uang


def tampilkan_laporan(hasil, pembeli):
    total_tiket, total_uang = hitung_total(hasil)

    baris = [[nama, terjual, rupiah(pendapatan)]
             for nama, (terjual, pendapatan) in hasil.items()]
    baris.append(["TOTAL", total_tiket, rupiah(total_uang)])
    tabel(["Kategori", "Terjual", "Pendapatan"], baris, judul="LAPORAN PENJUALAN TIKET")

    info(f"Jumlah pembeli    : {len(pembeli)}")
    if total_tiket > 0:
        terlaris = max(hasil, key=lambda nama: hasil[nama][0])
        info(f"Kategori terlaris : {terlaris}")


def tampilkan_diagram_batang(hasil, tampilkan_jendela=True):
    try:
        import matplotlib.pyplot as plt
        from matplotlib.ticker import MaxNLocator
    except ImportError:
        gagal("Library matplotlib belum terpasang. Jalankan: pip install matplotlib")
        return False

    nama_kategori = list(hasil)
    jumlah_terjual = [hasil[n][0] for n in nama_kategori]
    warna = ["#4C78A8", "#F58518", "#54A24B", "#E45756", "#72B7B2"]

    plt.figure(figsize=(7, 4.5))
    batang = plt.bar(nama_kategori, jumlah_terjual,
                     color=[warna[i % len(warna)] for i in range(len(nama_kategori))])
    for b, nilai in zip(batang, jumlah_terjual):
        plt.text(b.get_x() + b.get_width() / 2, b.get_height(), str(nilai),
                 ha="center", va="bottom", fontweight="bold")

    plt.title("Penjualan Tiket Konser Hindia per Kategori")
    plt.xlabel("Kategori Tiket")
    plt.ylabel("Jumlah Tiket Terjual")
    plt.ylim(0, max(jumlah_terjual + [1]) * 1.2)
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(file_grafik, dpi=120)

    if tampilkan_jendela:
        try:
            plt.show()
        except Exception:
            peringatan("Jendela grafik tidak bisa dibuka, grafik tetap disimpan di " + file_grafik)
    plt.close()
    return True


def simpan_laporan_teks(hasil, pembeli):
    total_tiket, total_uang = hitung_total(hasil)
    with open(file_laporan, "w", encoding="utf-8") as f:
        f.write("LAPORAN PENJUALAN TIKET KONSER HINDIA\n")
        f.write("Dibuat: " + waktu_sekarang() + "\n\n")
        for nama, (terjual, pendapatan) in hasil.items():
            f.write(f"{nama}: {terjual} tiket, {rupiah(pendapatan)}\n")
        f.write(f"\nTotal tiket     : {total_tiket}\n")
        f.write(f"Total pendapatan: {rupiah(total_uang)}\n")
        f.write(f"Jumlah pembeli  : {len(pembeli)}\n")
