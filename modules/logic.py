import re
import datetime
import textwrap
import io
import time
import random
from mutagen.mp3 import MP3
from modules.network import safe_request_get

# ==========================================
# TEXT & AUDIO PROCESSING LOGIC
# ==========================================

def format_time(seconds):
    """Konversi detik (float) ke format SRT timestamp (HH:MM:SS,mmm)"""
    td = datetime.timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60
    millis = int(td.microseconds / 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"

def smart_split_engine(text, total_duration, mode):
    """Mesin pemecah teks cerdas berdasarkan Mode (Waqaf, Ayat, Standard)"""
    results = []
    
    if mode == "WAQOF":
        # Tanda waqaf dalam Al-Quran
        waqof_marks = r"([ۗۚۛۖۙ۔۞])"
        parts = re.split(waqof_marks, text)
        chunks = []
        curr = ""
        
        for p in parts:
            curr += p
            if re.match(waqof_marks, p):
                chunks.append(curr.strip())
                curr = ""
        
        if curr.strip(): chunks.append(curr.strip())
        if not chunks: chunks = [text]
        
        # Hitung durasi proporsional
        total_len = sum(len(c) for c in chunks)
        for c in chunks:
            ratio = len(c)/total_len if total_len>0 else 1
            results.append({"text":c, "duration":total_duration*ratio})
            
    elif mode == "AYAT":
        # Full satu ayat
        results.append({"text": text, "duration": total_duration})
        
    else: 
        # Standard: pecah per karakter/kata jika terlalu panjang
        chunks = textwrap.wrap(text, 100)
        for c in chunks:
            results.append({"text":c, "duration": total_duration*(len(c)/len(text))})
            
    return results

def to_arabic_number(n):
    """Konversi angka latin ke angka Arab"""
    arabic_digits = "٠١٢٣٤٥٦٧٨٩"
    return "".join([arabic_digits[int(d)] for d in str(n)])

def process_single_ayah(idx, ayah_ar, ayah_tr, ayah_audio_url, start_ayah_num, mode_code, surah_num, surah_name):
    """Worker function untuk diproses di thread terpisah"""
    
    # Jeda acak 0.1 - 0.5 detik agar request tidak terlihat seperti serangan mesin
    time.sleep(random.uniform(0.1, 0.5)) 
    
    aud_data = None
    real_duration = 0
    
    # 1. Download Audio
    if ayah_audio_url:
        resp = safe_request_get(ayah_audio_url)
        if resp:
            aud_data = resp.content
            try:
                # Cek durasi asli dari MP3 header
                mp3_io = io.BytesIO(aud_data)
                real_duration = MP3(mp3_io).info.length
            except:
                real_duration = 0

    # 2. Fallback Duration (Estimasi jika download gagal)
    if real_duration == 0:
        # Rata-rata 0.12 detik per huruf Arab
        real_duration = max(3, len(ayah_ar['text']) * 0.12)

    # --- ADD BERSE NUMBER ---
    current_ayah = start_ayah_num + idx
    # Simbol "End of Ayah" (۝) + Nomor Arab
    ayah_suffix = f" ۝{to_arabic_number(current_ayah)}"
    full_text_with_num = ayah_ar['text'] + ayah_suffix

    # 3. Split Text
    # Kita kirim teks yang sudah ada nomor ayatnya ke engine
    chunks = smart_split_engine(full_text_with_num, real_duration, mode_code)
    
    # 4. Format Nama File: 001_AlFatihah_001.mp3
    sanitized_name = surah_name.replace(" ", "")
    filename_formatted = f"{surah_num:03d}_{sanitized_name}_{current_ayah:03d}.mp3"
    
    return {
        "index": idx,
        "filename": filename_formatted,
        "audio_data": aud_data,
        "duration": real_duration,
        "chunks": chunks,
        "text_tr": ayah_tr['text']
    }
