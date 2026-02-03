import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ==========================================
# NETWORK SECURITY LAYER (ANTI-BANNED)
# ==========================================

def get_session():
    """Membuat session dengan retry strategy"""
    session = requests.Session()
    # Retry 3 kali jika gagal, dengan jeda waktu (backoff)
    retry = Retry(
        total=3, 
        read=3, 
        connect=3, 
        backoff_factor=1, # Tunggu 1s, 2s, 4s...
        status_forcelist=[429, 500, 502, 503, 504] # Error yang boleh di-retry
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

def safe_request_get(url, params=None):
    """Fungsi Request Aman (Menyamar jadi Browser)"""
    session = get_session()
    # Headers agar dianggap browser Chrome asli (Bukan Bot)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Connection": "keep-alive"
    }
    
    try:
        response = session.get(url, headers=headers, params=params, timeout=20)
        response.raise_for_status() # Cek jika ada error HTTP
        return response
    except requests.exceptions.RequestException as e:
        # Jika gagal total, return None (biar tidak crash app)
        print(f"Request Error: {e}")
        return None
