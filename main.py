from database import buat_database, isi_data_awal
from utils import tampilkan_info_konser
from auth import register, login, login_admin
from pelanggan import menu_pelanggan
from petugas import menu_petugas
from admin import menu_admin

def main():
    buat_database()
    isi_data_awal()

test push