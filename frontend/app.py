# frontend/app.py
import streamlit as st
import requests

st.set_page_config(page_title="Lumina News KI", layout="wide")

# === Styling ===
st.markdown("""
<style>
body {
    background: radial-gradient(circle at top left, #0a0015, #1a001f, #0a0010);
    color: #eaeaea;
    font-family: 'Poppins', sans-serif;
}
h1 {
    text-align: center;
    font-size: 3rem;
    background: linear-gradient(90deg, #9d4edd, #ff00c8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 0 20px rgba(157, 78, 221, 0.6);
}
h3 { color: #e0aaff; }
.news-card {
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 18px;
    padding: 20px;
    margin: 14px 0;
    box-shadow: 0 0 10px rgba(157, 78, 221, 0.2);
    backdrop-filter: blur(8px);
    transition: all 0.3s ease;
}
.news-card:hover {
    transform: scale(1.03);
    box-shadow: 0 0 30px rgba(255, 0, 200, 0.5);
}
a {
    text-decoration: none;
    color: #9d4edd;
    font-weight: bold;
}
a:hover { color: #ff00c8; text-shadow: 0 0 8px #ff00c8; }
.stButton>button {
    background: linear-gradient(90deg, #9d4edd, #ff00c8);
    border: none;
    color: white;
    border-radius: 10px;
    padding: 0.5rem 1.2rem;
    font-size: 1rem;
    font-weight: bold;
    transition: all 0.3s ease;
}
.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 20px #ff00c8;
}
.stSelectbox, .stTextInput {
    background-color: rgba(0,0,0,0.3);
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

API_BASE = "http://127.0.0.1:8000"

st.markdown("<h1>🌌 Lumina News KI – Dark Neon Edition</h1>", unsafe_allow_html=True)
st.caption("Deine Zukunft in Nachrichtenform. Zweisprachig. Intelligent. Stilvoll. ⚡")

langs = {"🇩🇪 Deutsch": "de", "🇬🇧 English": "en"}
categories = ["general", "technology", "business", "sports", "science", "entertainment", "powi"]

col1, col2, col3 = st.columns(3)
with col1:
    language = langs[st.selectbox("🌐 Sprache / Language", list(langs.keys()))]
with col2:
    category = st.selectbox("🗂 Kategorie / Category", categories)
with col3:
    sort = st.selectbox("🔢 Sortierung / Sort by", ["newest", "importance"])

if st.button("🚀 Zeige Nachrichten / Show News"):
    with st.spinner("KI lädt die besten Artikel... 💫"):
        resp = requests.post(f"{API_BASE}/news", json={"language": language, "category": category, "sort_by": sort})
        if resp.status_code == 200:
            data = resp.json()
            st.success(f"✅ {data['count']} Artikel geladen ({data['language']})")
            for n in data["news"]:
                st.markdown(f"""
                <div class='news-card'>
                    <h3>{n['title']}</h3>
                    <p>{n['description']}</p>
                    <p><b>Quelle:</b> {n['source']} | <b>Datum:</b> {n['published_at']}</p>
                    <a href="{n['url']}" target="_blank">🌐 Weiterlesen</a>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.error("⚠ Fehler beim Laden der Nachrichten")
