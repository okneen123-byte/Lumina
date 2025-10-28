# streamlit_app.py
import streamlit as st
import requests

# 🔧 Hier Render-URL deines Backends eintragen
# Beispiel: https://lumina-backend.onrender.com
API_BASE = "https://luminanews-ai.onrender.com"

st.set_page_config(page_title="Lumina KI News", page_icon="📰", layout="centered")

st.title("🧠 Lumina KI – Personalisierte News")

# ---------------- AUTH ----------------
menu = ["Login", "Sign Up", "Personalisierte News", "Kategorien-News"]
choice = st.sidebar.selectbox("Menü", menu)

if "email" not in st.session_state:
    st.session_state.email = None
if "password" not in st.session_state:
    st.session_state.password = None

def signup():
    st.subheader("Neues Konto erstellen")
    email = st.text_input("E-Mail")
    password = st.text_input("Passwort", type="password")
    if st.button("Registrieren"):
        res = requests.post(f"{API_BASE}/signup", json={"email": email, "password": password})
        if res.status_code == 200:
            st.success("✅ Konto erstellt! Bitte jetzt einloggen.")
        else:
            st.error(res.json().get("detail", "Fehler bei Registrierung."))

def login():
    st.subheader("Login")
    email = st.text_input("E-Mail")
    password = st.text_input("Passwort", type="password")
    if st.button("Einloggen"):
        res = requests.post(f"{API_BASE}/login", json={"email": email, "password": password})
        if res.status_code == 200:
            st.session_state.email = email
            st.session_state.password = password
            st.success("✅ Erfolgreich eingeloggt!")
        else:
            st.error("❌ Ungültige Anmeldedaten.")

def show_personalized():
    if not st.session_state.email:
        st.warning("Bitte zuerst einloggen.")
        return

    st.subheader("✨ Deine Interessen")
    interests = st.text_input("Woran bist du interessiert? (z. B. KI, Politik, Gaming)")
    if st.button("Interessen speichern"):
        data = {"email": st.session_state.email, "interests": interests}
        res = requests.post(f"{API_BASE}/set_preferences", json=data)
        if res.status_code == 200:
            st.success("✅ Interessen gespeichert!")
        else:
            st.error("Fehler beim Speichern der Interessen.")

    st.divider()
    st.subheader("🧠 Personalisierte News")

    if st.button("Aktualisieren"):
        res = requests.post(f"{API_BASE}/news/personalized", json={"email": st.session_state.email})
        if res.status_code == 200:
            news_items = res.json().get("personalized_news", [])
            if not news_items:
                st.info("Keine personalisierten Artikel gefunden.")
            for n in news_items:
                st.markdown(f"### [{n['title']}]({n['url']})")
                st.write(n['description'])
                st.caption(f"📰 {n['source']} | 📅 {n['published_at']} | 🔥 Relevanz: {n['relevance_score']}")
                st.divider()
        else:
            st.error("Fehler beim Abrufen der personalisierten News.")

def show_category_news():
    if not st.session_state.email:
        st.warning("Bitte zuerst einloggen.")
        return

    st.subheader("📚 Kategorie-News")
    category = st.selectbox("Kategorie auswählen", ["general", "technology", "sports", "science", "business", "health"])
    language = st.selectbox("Sprache", ["en", "de"])
    sort_by = st.radio("Sortierung", ["newest", "important"])

    if st.button("News laden"):
        data = {
            "email": st.session_state.email,
            "password": st.session_state.password,
            "category": category,
            "language": language,
            "sort_by": sort_by,
            "limit": 20
        }
        res = requests.post(f"{API_BASE}/news", json=data)
        if res.status_code == 200:
            articles = res.json().get("news", [])
            if not articles:
                st.info("Keine Artikel gefunden.")
            for n in articles:
                st.markdown(f"### [{n['title']}]({n['url']})")
                st.write(n['description'])
                st.caption(f"📰 {n['source']} | 📅 {n['published_at']}")
                st.divider()
        else:
            st.error(res.json().get("detail", "Fehler beim Abrufen der News."))

# ---------------- ROUTING ----------------
if choice == "Sign Up":
    signup()
elif choice == "Login":
    login()
elif choice == "Personalisierte News":
    show_personalized()
elif choice == "Kategorien-News":
    show_category_news()
