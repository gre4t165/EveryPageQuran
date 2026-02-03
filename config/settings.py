# ==========================================
# 0. CONFIGURATION & CONSTANTS
# ==========================================

AVAILABLE_QARIS = {
    # --- 🌟 THE LEGENDS (EGYPTIAN CLASSICS) ---
    "Mahmoud Khalil Al-Husary (Murattal)": "ar.husary",
    "Mahmoud Khalil Al-Husary (Mujawwad - Slow)": "ar.husarymujawwad",
    "Abdul Basit Abdul Samad (Murattal)": "ar.abdulbasitmurattal",
    "Abdul Basit Abdul Samad (Mujawwad - Slow)": "ar.abdulbasitmujawwad",
    "Mohamed Siddiq Al-Minshawi (Murattal)": "ar.minshawi",
    "Mohamed Siddiq Al-Minshawi (Mujawwad - Slow)": "ar.minshawimujawwad",
    
    # --- 🕋 IMAMS OF HARAMAIN (MECCA & MADINAH) ---
    "Mishary Rashid Alafasy": "ar.alafasy",
    "Abdul Rahman Al-Sudais": "ar.abdulrahmanalsudais",
    "Saud Al-Shuraim": "ar.saudshuraim",
    "Maher Al Muaiqly": "ar.mahermuaiqly",
    "Yasser Al-Dosari": "ar.yasseraldossari",
    "Abdullah Awad Al-Juhany": "ar.abdullahjuhany",
    "Bandar Baleela": "ar.bandarbaleela",
    "Salah Al-Budair": "ar.salahbudair",
    "Ali Al-Hudaifi": "ar.hudaify",
    
    # --- 🕌 POPULAR & MODERN (GULF/LEVANT) ---
    "Abu Bakr Al Shatri": "ar.shatri",
    "Ahmed Al Ajmi": "ar.ajamy",
    "Saad Al Ghamdi": "ar.saadalghamdi",
    "Nasser Al Qatami": "ar.nasseralqatami",
    "Hani Ar-Rifai (Emotional)": "ar.hanirifai",
    "Fares Abbad": "ar.faresabbad",
    "Abdullah Basfar": "ar.abdullahbasfar",
    "Khalifa Al Tunaiji": "ar.tunaiji",
    "Muhammad Jibreel": "ar.muhammadjibreel",
    
    # --- 📚 LEARNING & CLEAR TAJWEED ---
    "Dr. Ayman Suwayd (Tajweed Master)": "ar.aymanswoaid",
    "Ibrahim Al-Akhdar": "ar.ibrahimakhbar",
    "Mahmoud Ali Al-Banna": "ar.mahmoudalibanna",
    
    # --- 🌍 OTHER STYLES ---
    "Abdullah Al-Matrood": "ar.abdullahmatroud",
    "Ahmed Al-Hawashi": "ar.ahmedalhawashi",
    "Ahmed Al-Trabulsi": "ar.ahmedtrabulsi",
    "Akram Al-Alaqmi": "ar.akramalaqmi"
}

AVAILABLE_EDITIONS = {
    # --- 🔠 TRANSLITERATION (PENTING BUAT PEMULA) ---
    "🔠 Transliteration (Latin Text)": "en.transliteration",

    # --- 🇮🇩 SOUTHEAST ASIA ---
    "🇮🇩 Indonesia - Kemenag RI": "id.indonesian",
    "🇮🇩 Indonesia - Jalalayn": "id.jalalayn",
    "🇲🇾 Malay - Basmeih": "ms.basmeih",
    "🇵🇭 Tagalog (Philippines)": "tl.tagalog", 
    "🇻🇳 Vietnamese - Rowi": "vi.rowi",        

    # --- 🇬🇧 ENGLISH (MAJOR VARIANTS) ---
    "🇬🇧 English - Sahih International": "en.sahih",
    "🇬🇧 English - Dr. Mustafa Khattab": "en.khattab",
    "🇬🇧 English - Yusuf Ali": "en.yusufali",
    "🇬🇧 English - Pickthall": "en.pickthall",
    "🇬🇧 English - Arberry": "en.arberry",
    "🇬🇧 English - Muhammad Asad": "en.asad",
    "🇬🇧 English - Maududi (Tafhim)": "en.maududi",

    # --- 🇸🇦 ARABIC & TAFSIR ---
    "🇸🇦 Arabic - Jalalayn": "ar.jalalayn",
    "🇸🇦 Arabic - Muyassar": "ar.muyassar",

    # --- 🇪🇺 EUROPEAN ---
    "🇫🇷 French - Hamidullah": "fr.hamidullah",
    "🇩🇪 German - Bubenheim & Elyas": "de.bubenheim",
    "🇪🇸 Spanish - Cortes": "es.cortes",
    "🇮🇹 Italian - Piccardo": "it.piccardo",
    "🇵🇹 Portuguese - El Hayek": "pt.elhayek",
    "🇳🇱 Dutch - Keyzer": "nl.keyzer",
    "🇸🇪 Swedish - Bernstrom": "sv.bernstrom",
    "🇳🇴 Norwegian - Einar Berg": "no.berg",
    "🇷🇺 Russian - Kuliev": "ru.kuliev",
    "🇷🇺 Russian - Elmir Kuliev": "ru.kuliev-audio",
    "🇧🇦 Bosnian - Korkut": "bs.korkut",
    "🇦🇱 Albanian - Nahi": "sq.nahi",
    "🇵🇱 Polish - Bielawskiego": "pl.bielawskiego",
    "🇨🇿 Czech - Hrbek": "cs.hrbek",
    "🇷🇴 Romanian - Grigore": "ro.grigore",
    "🇧🇬 Bulgarian": "bg.theophanov",

    # --- 🌏 SOUTH ASIA (INDIA/PAKISTAN/BANGLADESH) ---
    "🇵🇰 Urdu - Jalandhry": "ur.jalandhry",
    "🇵🇰 Urdu - Maududi": "ur.maududi",
    "🇮🇳 Hindi - Farooq Khan": "hi.farooq",
    "🇮🇳 Bengali - Muhiuddin Khan": "bn.bengali",
    "🇮🇳 Tamil - Jan Turst": "ta.tamil",
    "🇮🇳 Malayalam - Abdul Hameed": "ml.abdulhameed",
    "🇮🇳 Telugu - Sankala": "te.divya",
    "🇮🇳 Gujarati": "gu.shaikh",

    # --- 🌏 MIDDLE EAST & CENTRAL ASIA ---
    "🇹🇷 Turkish - Diyanet": "tr.diyanet",
    "🇮🇷 Persian - Ghomshei": "fa.ghomshei",
    "🇮🇷 Persian - Makarem Shirazi": "fa.makarem",
    "🇹🇯 Tajik": "tg.ayati",
    "🇺🇿 Uzbek - Mansour": "uz.sodik",
    "🇰🇿 Kazakh - Altape": "kk.altape",
    "🇦🇿 Azerbaijani - Musayev": "az.musayev",
    "IQ Kurdish - Asan": "ku.asan",
    "AF Pashto - Zakaria": "ps.abdulwali",
    "Tatartar": "tt.nugman",

    # --- 🌏 EAST ASIA ---
    "🇨🇳 Chinese - Ma Jian (Simplified)": "zh.jian",
    "🇨🇳 Chinese - Ma Jian (Traditional)": "zh.majian",
    "🇯🇵 Japanese - Ryoichi Mita": "ja.mita",
    "🇰🇷 Korean": "ko.korean",
    "🇹🇭 Thai - Complex": "th.thai",

    # --- 🌍 AFRICAN ---
    "🇸🇴 Somali - Abduh": "so.abduh",
    "🇸🇿 Swahili - Barwani": "sw.barwani",
    "🇳🇬 Hausa - Gumi": "ha.gumi",
    "Amharic (Ethiopia)": "am.sadiq"
}

# Link Donasi
LINK_SAWERIA = "https://saweria.co/aribs"
LINK_BMC     = "https://buymeacoffee.com/aribs"
LINK_PAYPAL  = "https://paypal.me/aribudisetiawan"
