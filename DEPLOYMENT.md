# Panduan Deployment QuranSRT

Aplikasi ini dibangun menggunakan **Python Streamlit**. Karena WordPress menggunakan PHP, Anda tidak bisa menginstall aplikasi ini *langsung* di dalam WordPress.

**Solusi:** Deploy aplikasi ke **Streamlit Cloud** (gratis), lalu tempel (embed) ke WordPress menggunakan **Iframe**.

---

## Tahap 1: Deploy ke Streamlit Cloud (Gratis)

### 1. Persiapan File
Pastikan di folder project Anda ada file `requirements.txt`. File ini memberi tahu server library apa saja yang dibutuhkan.
Isinya minimal harus ada:
```txt
streamlit
requests
mutagen
```

### 2. Upload ke GitHub
1.  Buat akun di [GitHub.com](https://github.com).
2.  Buat Repository baru (Public).
3.  Upload semua file project Anda (`main.py`, folder `modules/`, `config/`, `requirements.txt`) ke repository tersebut.

### 3. Connect ke Streamlit Cloud
1.  Buka [share.streamlit.io](https://share.streamlit.io/) dan login dengan GitHub.
2.  Klik **"New app"**.
3.  Pilih Repository GitHub yang baru Anda buat.
4.  Branch: `main`.
5.  Main file path: `main.py`.
6.  Klik **"Deploy!"**.

Tunggu sebentar, dan aplikasi Anda akan online dengan alamat seperti `https://quransrt.streamlit.app`.

---

## Tahap 2: Pasang di WordPress

Setelah aplikasi online, Anda bisa memasangnya di halaman WordPress Anda agar terlihat menyatu dengan website.

1.  Login ke Dashboard WordPress Anda.
2.  Buat **Page** atau **Post** baru.
3.  Tambahkan block **"Custom HTML"**.
4.  Copy-paste kode berikut (ganti URL-nya dengan URL aplikasi Streamlit Anda):

```html
<iframe 
    src="https://quransrt.streamlit.app/?embed=true" 
    height="800" 
    style="width:100%; border:none; border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);"
    scrolling="yes">
</iframe>
```

> **Tips:** Tambahkan `/?embed=true` di akhir link Streamlit untuk menghilangkan header garis merah dan hamburger menu bawaan Streamlit, sehingga tampilan lebih bersih di WordPress.

---

## Alternatif: Hosting Lain
Selain Streamlit Cloud, Anda juga bisa deploy di:
- **Hugging Face Spaces** (Gratis & Cepat)
- **Render.com**
- **Heroku**
- **Railway.app**
- **VPS Sendiri** (DigitalOcean/Linode) menggunakan Docker.
