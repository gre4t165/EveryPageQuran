import streamlit as st
from app_modules.network import safe_request_get

# ==========================================
# API DATA FETCHING
# ==========================================

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_surah_list():
    """Fetch list of all Surahs"""
    # Use safe_request_get
    resp = safe_request_get("http://api.alquran.cloud/v1/surah")
    if resp:
        data = resp.json()['data']
        return {
            s['number']: {
                "name": s['englishName'], 
                "label": f"{s['number']}. {s['englishName']} ({s['name']}) - {s['numberOfAyahs']} Verses",
                "count": s['numberOfAyahs']
            } for s in data
        }
    else:
        # Emergency data if API is down
        return {1: {"name": "Al-Fatihah", "label": "1. Al-Fatihah - 7 Verses", "count": 7}}

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_surah_text(surah_id, edition):
    """Fetch Verse text/audio per Surah"""
    try:
        url = f"http://api.alquran.cloud/v1/surah/{surah_id}/editions/{edition}"
        resp = safe_request_get(url)
        
        if resp and resp.status_code == 200:
            json_data = resp.json()
            if 'data' in json_data and len(json_data['data']) > 0:
                # Pastikan key 'ayahs' ada
                if 'ayahs' in json_data['data'][0]:
                    return json_data['data'][0]['ayahs']
        
        # Jika gagal atau data tidak lengkap
        print(f"Warning: Failed to fetch data for edition: {edition}")
        return None
        
    except Exception as e:
        print(f"API Error ({edition}): {e}")
        return None
