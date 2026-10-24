import os
import threading
import yt_dlp
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.utils import platform

# ============================ PENGATURAN ANDROID ============================
# Meminta izin akses penyimpanan dan internet jika berjalan di Android
if platform == 'android':
    from android.permissions import request_permissions, Permission
    request_permissions([
        Permission.READ_EXTERNAL_STORAGE, 
        Permission.WRITE_EXTERNAL_STORAGE, 
        Permission.INTERNET
    ])
    # Folder unduhan default Android
    DOWNLOAD_DIR = '/storage/emulated/0/Download/OyenindoDLP'
else:
    # Folder unduhan default Desktop (untuk pengujian di PC)
    DOWNLOAD_DIR = os.path.join(os.path.expanduser("~"), "Downloads", "OyenindoDLP")

# Pastikan folder penyimpanan tersedia
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


class MediaDownloaderApp(App):
    def build(self):
        self.title = "Oyenindo DLP (Mobile)"
        
        # Tata Letak Utama
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # 1. Input URL
        layout.add_widget(Label(text="Masukkan URL Konten (YouTube, TikTok, dll):", size_hint_y=None, height=30))
        self.url_input = TextInput(hint_text="https://...", multiline=False, size_hint_y=None, height=50)
        layout.add_widget(self.url_input)
        
        # 2. Pilihan Jenis Media
        layout.add_widget(Label(text="Pilih Jenis Media:", size_hint_y=None, height=30))
        self.type_spinner = Spinner(
            text='1. Video + Audio (MP4)',
            values=('1. Video + Audio (MP4)', '2. Audio Saja (MP3/M4A)'),
            size_hint_y=None, height=50
        )
        layout.add_widget(self.type_spinner)
        
        # 3. Label Status
        self.status_label = Label(
            text="Status: Siap.", 
            color=(0, 0.5, 1, 1), 
            size_hint_y=None, height=40,
            halign="center"
        )
        layout.add_widget(self.status_label)
        
        # 4. Tombol Unduh
        self.download_btn = Button(
            text="PROSES & UNDUH MEDIA", 
            size_hint_y=None, height=60,
            background_color=(0, 0.7, 0.3, 1)
        )
        self.download_btn.bind(on_press=self.start_download_thread)
        layout.add_widget(self.download_btn)
        
        # Ruang kosong di bawah
        layout.add_widget(Label())
        
        return layout

    # ---------- Pembaruan Antarmuka (Aman untuk Thread) ----------
    def update_status(self, text):
        Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', text))

    def enable_button(self, dt=None):
        self.download_btn.disabled = False
        self.download_btn.text = "PROSES & UNDUH MEDIA"

    def show_popup(self, title, message):
        def open_popup(dt):
            popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
            popup_label = Label(text=message, text_size=(300, None), halign='center', valign='middle')
            close_btn = Button(text="Tutup", size_hint_y=None, height=40)
            
            popup_layout.add_widget(popup_label)
            popup_layout.add_widget(close_btn)
            
            popup = Popup(title=title, content=popup_layout, size_hint=(0.8, 0.4))
            close_btn.bind(on_press=popup.dismiss)
            popup.open()
        Clock.schedule_once(open_popup)

    # ---------- Hook Progres yt-dlp ----------
    def progress_hook(self, d):
        if d['status'] == 'downloading':
            pct = d.get('_percent_str', '').strip()
            # Bersihkan kode warna terminal ANSI jika ada
            pct = pct.replace('\x1b[0;94m', '').replace('\x1b[0m', '')
            if pct:
                self.update_status(f"Status: Mengunduh... {pct}")
        elif d['status'] == 'finished':
            self.update_status("Status: Memproses file...")

    # ---------- Logika Unduhan ----------
    def start_download_thread(self, instance):
        url = self.url_input.text.strip()
        if not url:
            self.show_popup("Error", "URL tidak boleh kosong!")
            return
            
        media_type = self.type_spinner.text
        
        # Nonaktifkan tombol saat mengunduh
        self.download_btn.disabled = True
        self.download_btn.text = "MENGUNDUH..."
        self.update_status("Status: Mengambil informasi media...")
        
        # Jalankan di background agar UI tidak freeze
        threading.Thread(target=self.process_download, args=(url, media_type), daemon=True).start()

    def process_download(self, url, media_type):
        try:
            # Konfigurasi dasar yt-dlp
            ydl_opts = {
                'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
                'noplaylist': True,
                'quiet': True,
                'no_warnings': True,
                'progress_hooks': [self.progress_hook],
            }

            # Tentukan format berdasarkan pilihan pengguna
            if "Audio" in media_type and "Video" not in media_type:
                # Mode Audio Saja
                ydl_opts['format'] = 'bestaudio/best'
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
            else:
                # Mode Video + Audio
                # Untuk Android, seringkali kita mengunduh file yang sudah ter-mux (berisi video+audio)
                # karena FFmpeg eksternal mungkin belum terpasang sempurna di modul Android.
                ydl_opts['format'] = 'best[ext=mp4]/best'
            
            # Eksekusi unduhan
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                
            self.update_status("Status: Selesai!")
            self.show_popup("Sukses", f"File berhasil disimpan di:\n{DOWNLOAD_DIR}")

        except Exception as e:
            self.update_status("Status: Terjadi kesalahan.")
            self.show_popup("Error", f"Gagal mengunduh:\n{str(e)[:150]}...")
            
        finally:
            # Aktifkan kembali tombol
            Clock.schedule_once(self.enable_button)

if __name__ == '__main__':
    MediaDownloaderApp().run()