# frontend/app.py
import streamlit as st
import requests
from datetime import datetime

# ---------- Config ----------
API_BASE = st.secrets.get("API_BASE") or "http://127.0.0.1:8000"  # In Produktion: setze Streamlit secret API_BASE auf dein Backend-URL
CATEGORIES = ["general", "technology", "business", "sports", "science", "entertainment"]
LANGS = {"Deutsch":"de", "English":"en"}

# ---------- Texts (DE/EN) ----------
TEXT = {
    "de": {
        "title": "Lumina News KI 📰",
        "subtitle": "Personalisierte Nachrichten — aktuell, sortierbar & sicher",
        "email": "E-Mail",
        "password": "Passwort",
        "signup": "Registrieren",
        "login": "Anmelden",
        "logout": "Abmelden",
        "category": "Kategorie",
        "language": "Sprache",
        "sort": "Sortieren nach",
        "sort_newest": "Neueste",
        "sort_importance": "Wichtigkeit",
        "fetch": "News abrufen",
        "upgrade": "Premium",
        "welcome": "Willkommen",
        "no_news": "Keine News gefunden.",
        "trial_exhausted": "Free Trial Limit erreicht. Bitte Premium buchen."
    },
    "en": {
        "title": "Lumina News AI 📰",
        "subtitle": "Personalized news — fresh, sortable & secure",
        "email": "Email",
        "password": "Password",
        "signup": "Sign up",
        "login": "Log in",
        "logout": "Log out",
        "category": "Category",
        "language": "Language",
        "sort": "Sort by",
        "sort_newest": "Newest",
        "sort_importance": "Importance",
        "fetch": "Fetch news",
        "upgrade": "Premium",
        "welcome": "Welcome",
        "no_news": "No news found.",
        "trial_exhausted": "Free trial limit reached. Please upgrade to Premium."
    }
}

# ---------- Session state ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "email" not in st.session_state:
    st.session_state.email = ""
if "lang" not in st.session_state:
    st.session_state.lang = "de"

# ---------- Layout ----------
st.set_page_config(page_title="Lumina News KI", layout="wide")
col1, col2 = st.columns([3,1])
with col1:
    st.markdown(f"## {TEXT[st.session_state.lang]['title']}")
    st.write(TEXT[st.session_state.lang]['subtitle'])
with col2:
    # language switch
    choice = st.selectbox(" ", list(LANGS.keys()), index=0 if st.session_state.lang=="de" else 1)
    st.session_state.lang = LANGS[choice]

texts = TEXT[st.session_state.lang]

# ---------- Auth box ----------
with st.expander(texts["welcome"] if st.session_state.logged_in else texts["login"], expanded=True):
    if not st.session_state.logged_in:
        # login or signup
        col_a, col_b = st.columns(2)
        with col_a:
            email = st.text_input(texts["email"], key="input_email")
            password = st.text_input(texts["password"], type="password", key="input_password")
        with col_b:
            if st.button(texts["login"]):
                if not email or not password:
                    st.warning("Bitte E-Mail & Passwort eingeben." if st.session_state.lang=="de" else "Please enter email & password.")
                else:
                    try:
                        r = requests.post(f"{API_BASE}/login", json={"email": email, "password": password}, timeout=10)
                        if r.status_code == 200:
                            st.session_state.logged_in = True
                            st.session_state.email = email
                            st.success("Erfolgreich eingeloggt." if st.session_state.lang=="de" else "Logged in successfully.")
                        else:
                            st.error(r.json().get("detail","Login failed."))
                    except Exception as e:
                        st.error(f"Fehler: {e}")
            if st.button(texts["signup"]):
                if not email or not password:
                    st.warning("Bitte E-Mail & Passwort eingeben." if st.session_state.lang=="de" else "Please enter email & password.")
                else:
                    try:
                        r = requests.post(f"{API_BASE}/signup", json={"email": email, "password": password}, timeout=10)
                        if r.status_code == 200:
                            st.success("Registrierung erfolgreich. Jetzt einloggen." if st.session_state.lang=="de" else "Signup successful. Please log in.")
                        else:
                            st.error(r.json().get("detail","Signup failed."))
                    except Exception as e:
                        st.error(f"Fehler: {e}")
    else:
        st.write(f"{st.session_state.email}")
        if st.button(texts["logout"]):
            st.session_state.logged_in = False
            st.session_state.email = ""

st.sidebar.header(texts["category"])
category = st.sidebar.selectbox("", CATEGORIES)
lang_label = st.sidebar.selectbox(texts["language"], list(LANGS.keys()))
language = LANGS[lang_label]
sort_choice = st.sidebar.selectbox(texts["sort"], [texts["sort_newest"], texts["sort_importance"]])
sort_by = "newest" if sort_choice==texts["sort_newest"] else "importance"
limit = st.sidebar.slider("Anzahl Artikel", 5, 50, 20)

# ---------- Fetch button ----------
if st.button(texts["fetch"]):
    if not st.session_state.logged_in:
        st.warning("Bitte einloggen." if st.session_state.lang=="de" else "Please log in.")
    else:
        payload = {
            "email": st.session_state.email,
            "password": st.session_state.get("input_password",""),  # Streamlit stores the typed password in session while logged in
            "category": category,
            "language": language,
            "sort_by": sort_by,
            "limit": limit
        }
        try:
            resp = requests.post(f"{API_BASE}/news", json=payload, timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                news = data.get("news", [])
                if not news:
                    st.info(texts["no_news"])
                else:
                    # display cards
                    for n in news:
                        with st.container():
                            st.markdown(f"### [{n['title']}]({n['url']})")
                            st.write(f"{n.get('source','')}, {n.get('published_at','')}")
                            # importance bar
                            importance = n.get("importance", 0)
                            st.progress(int(importance*100))
                            st.write(n.get("description",""))
                            st.markdown("---")
            else:
                # show error message
                detail = resp.json().get("detail", "Fehler")
                if resp.status_code == 403 and "Free trial limit" in detail:
                    st.error(texts["trial_exhausted"])
                else:
                    st.error(detail)
        except Exception as e:
            st.error(f"Fehler beim Abrufen: {e}")
