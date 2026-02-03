import streamlit as st
import io
import gc
import zipfile
import textwrap
from concurrent.futures import ThreadPoolExecutor, as_completed

# --- IMPORT MODULES ---
# --- IMPORT MODULES ---
from app_config.settings import AVAILABLE_QARIS, AVAILABLE_EDITIONS, LINK_SAWERIA, LINK_BMC, LINK_PAYPAL
from app_config.translations import TRANSLATIONS
from app_modules.api import fetch_surah_list, fetch_surah_text
from app_modules.logic import format_time, process_single_ayah

# ==========================================
# 1. PAGE SETUP & THEME STATE
# ==========================================

st.set_page_config(
    page_title="EveryPage Quran",
    page_icon="📖",
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# Cek Theme State (Default: Dark)
if 'theme_mode' not in st.session_state:
    st.session_state.theme_mode = True

# Cek Language State (Default: English)
if 'ui_lang' not in st.session_state:
    st.session_state.ui_lang = "English"

# Load current language dictionary
ui_text = TRANSLATIONS[st.session_state.ui_lang]

# Define Color Palettes
if st.session_state.theme_mode: # DARK MODE
    bg_color = "#020617"
    card_color = "#0f172a" 
    text_color = "#f8fafc"
    sub_text_color = "#94a3b8"
    border_color = "#1e293b"
    input_bg = "#1e293b"
    accent_color = "#3b82f6"
    container_border = "1px solid #1e293b"
else: # LIGHT MODE
    bg_color = "#f8fafc"
    card_color = "#ffffff"
    text_color = "#0f172a"
    sub_text_color = "#334155" # Darker subtext for visibility
    border_color = "#e2e8f0"
    input_bg = "#f1f5f9"
    accent_color = "#2563eb"
    container_border = "1px solid #e2e8f0"

# Apply Dynamic CSS
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Amiri:wght@400;700&display=swap');
    
    html, body, [class*="css"] {{
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: {text_color};
    }}
    .stApp {{ background-color: {bg_color}; }}
    
    /* Caption text visibility fix */
    .stCaption {{
        color: {sub_text_color} !important;
        font-weight: 600 !important;
        opacity: 1 !important;
    }}

    /* Main Area Padding */
    .block-container {{ max-width: 800px; padding-top: 2rem; padding-bottom: 3rem; }}

    /* Typography */
    h1 {{ color: {text_color} !important; }}
    
    /* INPUT FIELDS STYLING */
    .stSelectbox div[data-baseweb="select"] > div, 
    .stNumberInput input, 
    .stTextInput input {{
        background-color: {input_bg} !important; 
        color: {text_color} !important;
        border: 1px solid {border_color} !important; 
        border-radius: 10px !important;
        height: 45px;
        font-weight: 600;
    }}
    
    /* Labels (General) */
    .stSelectbox label, .stNumberInput label, .stTextInput label {{
        color: {sub_text_color} !important;
        font-size: 0.85rem !important;
        margin-bottom: 0.3rem !important;
    }}
    
    /* TOGGLE & CHECKBOX VISIBILITY FIX */
    div[data-testid="stCheckbox"] label span p, 
    div[data-testid="stCheckbox"] label p {{
        color: {text_color} !important;
        font-weight: 700 !important;
    }}
    div[data-testid="stCheckbox"] span[role="checkbox"] {{
        border: 1px solid {border_color};
    }}

    /* GENERATE BUTTON */
    div.stButton > button {{
        background: linear-gradient(90deg, #F59E0B 0%, #D97706 100%);
        color: white !important; font-weight: 800; border-radius: 12px;
        border: none;
        height: 50px;
        margin-top: 15px; /* Alignment fix */
        box-shadow: 0 4px 15px rgba(245, 158, 11, 0.4);
        transition: all 0.2s ease;
    }}
    div.stButton > button:hover {{ transform: scale(1.02); box-shadow: 0 8px 20px rgba(245, 158, 11, 0.5); }}

    /* Custom Containers */
    [data-testid="stVerticalBlockBorderWrapper"] {{
        background-color: {card_color};
        border-radius: 16px;
        border: {container_border};
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        padding: 20px;
        margin-bottom: 20px;
    }}

    /* Footer & Hide */
    #MainMenu {{visibility: hidden;}} footer {{visibility: hidden;}} header {{visibility: hidden;}}
    </style>
""", unsafe_allow_html=True)


# ==========================================
# 2. PAGE LAYOUT
# ==========================================

# A. Header Modern (CSS Logo + Language + Theme)
col_h1, col_h2, col_h3 = st.columns([5.5, 1.5, 1])

with col_h1:
    # High-End Typographic Logo with SVG Icon
    svg_icon = """
    <svg width="42" height="42" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 10px;">
        <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path>
        <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path>
    </svg>
    """
    
    logo_html = f"""
    <div style="display: flex; align-items: center; margin-bottom: 5px;">
        <div style="color: {accent_color};">{svg_icon}</div>
        <div style="font-family: 'Plus Jakarta Sans', sans-serif; letter-spacing: -1px; line-height: 1;">
            <span style="font-size: 2.2rem; font-weight: 800; color: {text_color};">EveryPage</span>
            <span style="font-size: 2.2rem; font-weight: 400; color: {sub_text_color};">Quran</span>
        </div>
    </div>
    """
    st.markdown(logo_html, unsafe_allow_html=True)

with col_h2:
    # LANGUAGE SELECTOR
    st.markdown("<div style='height: 5px;'></div>", unsafe_allow_html=True)
    sel_lang = st.selectbox(
        "Lang", 
        list(TRANSLATIONS.keys()), 
        index=list(TRANSLATIONS.keys()).index(st.session_state.ui_lang),
        label_visibility="collapsed"
    )
    if sel_lang != st.session_state.ui_lang:
        st.session_state.ui_lang = sel_lang
        st.rerun()

with col_h3:
    # THEME TOGGLE
    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    is_dark = st.toggle("Dark", value=st.session_state.theme_mode, key="theme_toggle")
    if is_dark != st.session_state.theme_mode:
        st.session_state.theme_mode = is_dark
        st.rerun()

st.markdown("<div style='margin-bottom: 1rem;'></div>", unsafe_allow_html=True)

# LOAD DATA
surah_data_full = fetch_surah_list()
surah_options = list(surah_data_full.keys())

# --- BLOCK 1: SELECTION & ACTION ---
# Use st.container with border to group main inputs
with st.container(border=True):
    c_main1, c_main2 = st.columns([2.5, 1])
    
    with c_main1:
        # Surah Selection
        selected_num = st.selectbox(
            ui_text['select_surah'], 
            surah_options, 
            format_func=lambda x: surah_data_full[x]["label"],
        )
        total_ayahs = surah_data_full[selected_num]["count"]

        # Verse Range (Nested Columns for tight layout)
        c_v1, c_v2 = st.columns(2)
        with c_v1:
            start_val = st.number_input(ui_text['start_verse'], min_value=1, value=1)
        with c_v2:
            end_val = st.number_input(ui_text['end_verse'], min_value=1, value=total_ayahs, max_value=total_ayahs)
            if start_val > end_val: start_val = end_val

    with c_main2:
        # Big Generate Button vertically aligned
        st.markdown("<div style='height: 26px;'></div>", unsafe_allow_html=True) # Spacer label
        # Spacer to push button down little bit for visual alignment
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True) 
        do_generate = st.button(ui_text['generate_btn'], use_container_width=True)
        # Small info text
        st.caption(ui_text['total_verses'].format(end_val - start_val + 1))


# --- BLOCK 2: OPTIONS & SETTINGS ---
with st.container(border=True):
    col_opt1, col_opt2, col_opt3 = st.columns([1.5, 1.5, 1])
    
    with col_opt1:
        qari_key = st.selectbox(ui_text['reciter'], list(AVAILABLE_QARIS.keys()))
        
    with col_opt2:
        trans_key = st.selectbox(ui_text['translation'], list(AVAILABLE_EDITIONS.keys()))

    with col_opt3:
        # Compact extra options
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True) # visual balance
        include_audio = st.checkbox(ui_text['download_mp3'], value=False)
        
        # Popover for advanced mode
        split_mode = st.popover(ui_text['mode_settings'], use_container_width=True)
        split_opt = split_mode.radio(ui_text['split_mode'], ["WAQOF (Auto)", "VERSE (Full)", "STD"], index=0)
        mode_code = "WAQOF" if "WAQOF" in split_opt else ("AYAT" if "VERSE" in split_opt else "STD")


# ==========================================
# 3. RESULT LOGIC
# ==========================================

if do_generate:
    progress_qube = st.empty()
    progress_qube.progress(0, "Connecting...")
    
    try:
        qari_code = AVAILABLE_QARIS[qari_key]
        trans_code = AVAILABLE_EDITIONS[trans_key]
        surah_name_en = surah_data_full[selected_num]["name"]
        
        with st.spinner(ui_text['processing']):
            full_ar = fetch_surah_text(selected_num, "quran-simple")
            full_tr = fetch_surah_text(selected_num, trans_code)
            full_au = fetch_surah_text(selected_num, qari_code)

            if not full_ar:
                st.error(ui_text['error_api'])
                st.stop()
            
            # Fallback Logic
            if not full_tr:
                st.warning(ui_text['warn_trans'])
                full_tr = full_ar 
            
            has_audio = True
            if not full_au:
                st.warning(ui_text['warn_audio'])
                has_audio = False
                full_au = [{'audio': None} for _ in range(len(full_ar))]

            s_idx = start_val - 1
            e_idx = end_val
            ayahs_ar = full_ar[s_idx:e_idx]
            ayahs_tr = full_tr[s_idx:e_idx]
            ayahs_au = full_au[s_idx:e_idx]
            
            total_items = len(ayahs_ar)
            results_holder = [None] * total_items
            
            with ThreadPoolExecutor(max_workers=min(8, total_items)) as executor:
                futures = []
                for i in range(total_items):
                    # Safety check
                    aud_url = ayahs_au[i].get('audio') if has_audio and ayahs_au[i] else None
                    
                    futures.append(executor.submit(
                        process_single_ayah, i, ayahs_ar[i], ayahs_tr[i], aud_url,
                        start_val, mode_code, selected_num, surah_name_en
                    ))
                
                done_c = 0
                for f in as_completed(futures):
                    res = f.result()
                    results_holder[res['index']] = res
                    done_c += 1
                    progress_qube.progress(int((done_c/total_items)*100), f"Processing {done_c}/{total_items}...")

        srt_ar, srt_tr, preview_log = "", "", ""
        counter = 1; timer = 0.0; audio_buffer = []

        for item in results_holder:
            if include_audio and item['audio_data']: audio_buffer.append(item)
            for cx, ch in enumerate(item['chunks']):
                t_s = format_time(timer); t_e = format_time(timer + ch['duration'])
                block = f"{counter}\n{t_s} --> {t_e}\n"
                srt_ar += f"{block}{ch['text']}\n\n"
                tr_txt = item['text_tr'] if cx == 0 else "..."
                if len(item['chunks']) > 1 and cx == 0: tr_txt = textwrap.shorten(tr_txt, 60)
                srt_tr += f"{block}{tr_txt}\n\n"
                preview_log += f"[{t_s}] {ch['text']}\n"
                timer += ch['duration']; counter += 1
        
        progress_qube.empty()

        # ZIP & Download
        zip_mem = io.BytesIO()
        with zipfile.ZipFile(zip_mem, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr(f"{selected_num:03d}_{surah_name_en}_Ar.srt", srt_ar)
            zf.writestr(f"{selected_num:03d}_{surah_name_en}_Tr.srt", srt_tr)
            if include_audio:
                for a in audio_buffer: zf.writestr(f"Audio/{a['filename']}", a['audio_data'])
        
        # Result Container
        with st.container(border=True):
            cols_res = st.columns([1, 2])
            with cols_res[0]:
                st.success(ui_text['success'])
                st.download_button(ui_text['download_zip'], zip_mem.getvalue(), f"QuranSRT_{surah_name_en}.zip", "application/zip", type="primary", use_container_width=True)
            with cols_res[1]:
                st.text_area(ui_text['preview'], preview_log, height=100, label_visibility="collapsed")

    except Exception as e:
        st.error(f"Error: {e}")

# ==========================================
# 4. FOOTER & DONATION (Compact Version)
# ==========================================
st.markdown("<div style='margin-top: 1.5rem; border-top: 1px dashed rgba(100,100,100,0.15); margin-bottom: 1rem;'></div>", unsafe_allow_html=True)

# Layout 3 Columns tighter for small buttons
c_don1, c_don2, c_don3 = st.columns([1, 1, 1])

# Logo URLs
saweria_img = "https://saweria.co/favicon.ico"
bmc_logo = "https://cdn.buymeacoffee.com/buttons/bmc-new-btn-logo.svg"
paypal_logo = "https://www.paypalobjects.com/webstatic/mktg/logo/pp_cc_mark_37x23.jpg" # atau logo putih custom

with c_don1:
    st.markdown(f"""
    <a href="{LINK_SAWERIA}" target="_blank" style="text-decoration: none;">
        <div style="background-color: #faae2b; padding: 6px 10px; border-radius: 6px; color: #5a4b12; font-family: sans-serif; font-size: 0.85rem; font-weight: 800; text-align: center; display: flex; align-items: center; justify-content: center; gap: 6px; border: 1.5px solid #5a4b12; height: 38px; transition: transform 0.1s;">
            <img src="{saweria_img}" width="16" height="16" style="border-radius: 3px;"> SAWERIA
        </div>
    </a>
    """, unsafe_allow_html=True)

with c_don2:
    st.markdown(f"""
    <a href="{LINK_BMC}" target="_blank" style="text-decoration: none;">
        <div style="background-color: #FFDD00; padding: 6px 10px; border-radius: 6px; text-align: center; height: 38px; display: flex; align-items: center; justify-content: center; border: 1px solid rgba(0,0,0,0.1); transition: transform 0.1s;">
             <img src="{bmc_logo}" alt="BMC" style="height: 20px !important;">
             <span style="font-family:'Cookie', cursive; font-size: 1.1rem; margin-left: 6px; color: #000000; font-weight: 700; line-height: 1;">Buy me a coffee</span>
        </div>
    </a>
    """, unsafe_allow_html=True)

with c_don3:
    # PayPal Official Blue Button Style
    st.markdown(f"""
    <a href="{LINK_PAYPAL}" target="_blank" style="text-decoration: none;">
        <div style="background-color: #0070BA; padding: 6px 10px; border-radius: 6px; color: white; font-family: sans-serif; font-size: 0.85rem; font-weight: 700; text-align: center; display: flex; align-items: center; justify-content: center; gap: 8px; height: 38px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); transition: transform 0.1s;">
            <svg class="pp-logo" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="18" height="18" style="fill:white;">
                <path d="M7.076 21.337H2.47a.641.641 0 0 1-.633-.74L4.944.901C5.026.382 5.474 0 5.998 0h7.46c2.57 0 4.578.543 5.69 1.81 1.01 1.15 1.304 2.42 1.012 4.287-.023.143-.047.288-.077.437-.946 5.05-4.336 6.73-8.336 6.73h-1.037l-1.406 8.853-.19.964a.645.645 0 0 1-.632.518H7.076z"/>
            </svg>
            <span style="font-style: italic; font-weight: 800; letter-spacing: 0.5px;">PayPal</span>
        </div>
    </a>
    """, unsafe_allow_html=True)

st.markdown(f"<div style='text-align:right; font-size:0.75rem; color:{sub_text_color}; margin-top:15px; opacity: 0.8;'>{ui_text['footer_copyright']}</div>", unsafe_allow_html=True)
