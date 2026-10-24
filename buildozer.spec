[app]
title = OyenindoDLP
package.name = oyenindodlp
package.domain = org.oyenindo
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy
orientation = portrait
fullscreen = 0
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 24
android.ndk = 25b
android.allow_backup = True
# Ini kode agar tidak nyangkut nunggu persetujuan lisensi
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
p4a.branch = master
