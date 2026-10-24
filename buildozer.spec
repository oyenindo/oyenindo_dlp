[app]

# (str) Judul aplikasi Anda
title = OyenindoDLP

# (str) Nama package aplikasi
package.name = oyenindodlp

# (str) Domain package (tanpa spasi/simbol aneh)
package.domain = org.oyenindo

# (str) Direktori tempat source code utama berada
source.dir = .

# (list) Ekstensi file yang akan dimasukkan ke dalam APK
source.include_exts = py,png,jpg,kv,atlas

# (str) Versi aplikasi
version = 0.1

# (list) Kebutuhan pustaka aplikasi (cukup python3 dan kivy agar build mulus)
requirements = python3,kivy

# (str) Orientasi layar aplikasi (portrait / landscape)
orientation = portrait

# (int) Layar penuh (1 = ya, 0 = tidak)
fullscreen = 0

# (list) Izin akses Android yang dibutuhkan
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (int) Target API Android
android.api = 33

# (int) API minimum Android yang didukung
android.minapi = 24

# (str) Versi Android NDK yang stabil untuk menghindari error kompilasi
android.ndk = 25b

# (list) Arsitektur prosesor target
android.archs = arm64-v8a, armeabi-v7a

# (bool) Izinkan cadangan data aplikasi
android.allow_backup = True

[buildozer]

# (int) Level log (0 = error saja, 1 = info, 2 = debug)
log_level = 2

# (int) Peringatan jika dijalankan sebagai root (1 = ya, 0 = tidak)
warn_on_root = 1

# Menggunakan branch master untuk stabilitas toolchain
p4a.branch = master
