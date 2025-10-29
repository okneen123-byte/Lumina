# streamlit_app.py
import streamlit as st
import requests
import os

# ---------- KONFIG ----------
BACKEND_URL = os.getenv("BACKEND_URL", "https://dein-backend.onrender.com")

st.set_page_config(page_title="Lumina News KI", page_icon="📰", layout="centered")

# ---------- SESSION ----------
if "email" not in st.session_state:
    st.session_state.email = None
if "password" not in st.session_state:
    st.session_state.password = None
if "is_paid" not in st.session_state:
    st.session_state.is_paid = False

# ---------- FUNKTIONEN ----------
def signup(email, password):
    res = requests.post(f"{BACKEND_URL}/signup", json={"email": email, "password": password})
    return res.json() if res.status_code == 200 else {"error": res.text}

def login(email, password):
    res = requests.post(f"{BACKEND_URL}/login", json={"email": email, "password": password})
    if res.status_code == 200:
        data = res.json()
        st.session_state.email = email
        st.session_state.password = password
        st.session_state.is_paid = data.get("is_paid", False)
        return True
    else:
        st.error("❌ Falsche Zugangsdaten.")
        return False

def get_news(category="general", language="en", sort_by="newest"):
    body = {
        "email": st.session_state.email,
        "password": st.session_state.password,
        "category": category,
        "language": language,
        "sort_by": sort_by,
    }
    res = requests.post(f"{BACKEND_URL}/news", json=body)
    if res.status_code == 200:
        return res.json().get("news", [])
    else:
        st.error("Fehler beim Laden der News.")
        return []


# ---------- UI ----------
st.title("🧠 Lumina News KI")

if not st.session_state.email:
    st.subheader("🔑 Anmeldung oder Registrierung")

    choice = st.radio("Was möchtest du tun?", ["Einloggen", "Registrieren"])
    email = st.text_input("E-Mail")
    password = st.text_input("Passwort", type="password")

    if st.button("Weiter"):
        if choice == "Registrieren":
            out = signup(email, password)
            if "error" not in out:
                st.success("✅ Benutzer erfolgreich erstellt! Bitte einloggen.")
        else:
            if login(email, password):
                st.success(f"Willkommen, {email}!")
else:
    st.success(f"Angemeldet als {st.session_state.email}")
    st.sidebar.subheader("⚙ Optionen")
    category = st.sidebar.selectbox(
        "Kategorie",
        ["general", "technology", "business", "sports", "entertainment", "science", "health"],
    )
    language = st.sidebar.selectbox("Sprache", ["en", "de", "fr", "es"])
    sort_by = st.sidebar.radio("Sortierung", ["newest", "importance"])

    if st.button("📰 News laden"):
        with st.spinner("Lade aktuelle Artikel..."):
            news_list = get_news(category, language, sort_by)

        if not news_list:
            st.warning("Keine News gefunden.")
        else:
            for n in news_list:
                st.markdown(f"### [{n['title']}]({n['url']})")
                if n.get("description"):
                    st.write(n["description"])
                st.caption(f"📍 {n.get('source', 'Unbekannt')} — 🕓 {n.get('published_at', '')}")
                st.divider()

    if st.button("🚪 Abmelden"):
        st.session_state.email = None
        st.session_state.password = None
        st.experimental_rerun()
