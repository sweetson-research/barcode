import streamlit as st
import pandas as pd
from db import add_item, get_all

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Inventory System", layout="wide")

# ---------------- CLEAN UI ----------------
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.stApp {
    background-color: #0f0f0f;
    color: white;
}

.title {
    font-size: 32px;
    font-weight: bold;
}

.card {
    background-color: #1a1a1a;
    padding: 15px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOGIN ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if (
            username == st.secrets["auth"]["username"]
            and password == st.secrets["auth"]["password"]
        ):
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid credentials")

# ---------------- DASHBOARD ----------------
def dashboard():
    st.markdown('<div class="title">📊 Dashboard</div>', unsafe_allow_html=True)

    data = get_all()
    df = pd.DataFrame(data)

    if df.empty:
        st.info("No data yet")
        return

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Scans", len(df))
    col2.metric("Unique Barcodes", df["barcode"].nunique())
    col3.metric("Item Types", df["item_name"].nunique())

    st.divider()
    st.dataframe(df, use_container_width=True)

# ---------------- SCANNER ----------------
def scanner():
    st.markdown('<div class="title">📦 Scan Item</div>', unsafe_allow_html=True)

    if "last_barcode" not in st.session_state:
        st.session_state.last_barcode = ""

    barcode = st.text_input("Scan Barcode", placeholder="Scan using scanner...")
    item_name = st.text_input("Item Name (optional)")

    if barcode and barcode != st.session_state.last_barcode:
        add_item(barcode, item_name if item_name else "Unknown")
        st.session_state.last_barcode = barcode
        st.success(f"Saved: {barcode}")

# ---------------- MAIN ----------------
if not st.session_state.logged_in:
    login()
else:
    st.markdown('<div class="title">📦 Inventory System</div>', unsafe_allow_html=True)
    st.caption("Developed by Sweetson Joseph")

    menu = st.sidebar.radio("Menu", ["Dashboard", "Scan Item"])

    if menu == "Dashboard":
        dashboard()
    elif menu == "Scan Item":
        scanner()

    st.divider()
    st.caption("© 2026 Sweetson Joseph")
