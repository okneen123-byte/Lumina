# frontend/app.py
import streamlit as st
import requests

st.set_page_config(page_title="Lumina News KI", layout="wide")

# === Styling ===
st.markdown("""
<style>
body { background: linear-gradient(180deg, #e0f7fa, #ffffff); font-family: 'Poppins', sans-serif; }
h1 { color: #ff006e; text-align:center; animation: glow 2s ease-in-out infinite alternate; }
@keyframes glow { from { text-shadow: 0 0 10px #ff4d6d; } to { text-shadow: 0 0 25px #ffb3c1; } }
.news-card {
    background: #ffffff;
    border-radius: 16px;
    padding: 18px;
    margin: 12px 0;
    box-shadow: 0 4px 10px rgba(0,0,0,0.08);
    transition: all 0.3s ease;
}
.news-card:hover {
    transform: scale(1.02);
    box-shadow: 0 6px 18px rgba(0,0,0,0.15);
}
a { text-decoration: none; color: #0077b6; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

API_BASE = "http://127.0.0.1:8000"

st.markdown("<h1>📰 Lumina News KI – Deluxe Edition</h1>", unsafe_allow_html=True)
st.caption("Deine persönliche Nachrichtenwelt – zweisprachig, intelligent & wunderschön 💫")

langs = {"Deutsch": "de", "English": "en"}
categories = ["general", "technology", "business", "sports", "science", "entertainment", "powi"]

col1, col2, col3 = st.columns(3)
with col1:
    language = langs[st.selectbox("🌐 Sprache / Language", list(langs.keys()))]
with col2:
    category = st.selectbox("🗂 Kategorie / Category", categories)
with col3:
    sort = st.selectbox("🔢 Sortierung / Sort by", ["newest", "importance"])

if st.button("✨ Zeige Nachrichten / Show News"):
    with st.spinner("Lade aktuelle Artikel..."):
        resp = requests.post(f"{API_BASE}/news", json={"language": language, "category": category, "sort_by": sort})
        if resp.status_code == 200:
            data = resp.json()
            st.success(f"✅ {data['count']} Artikel gefunden ({data['language']})")
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
            st.error("Fehler beim Laden der Nachrichten 😕"
