import streamlit as st
import pandas as pd
from db import add_item, get_all

# ---------------- CONFIG ----------------
st.set_page_config(page_title="BMS 3.12", layout="wide")

# ---------------- LOGIN ----------------
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

# ---------------- HEADER ----------------
def header():
    col1, col2 = st.columns([1, 6])

    with col1:
        st.image("logo.png", width=70)

    with col2:
        st.markdown("### BMS 3.12")
        st.caption("Codex MSD365 F&O - Developed by Sweetson Joseph")

# ---------------- DASHBOARD ----------------
def dashboard():
    st.subheader("📊 Dashboard")

    data = get_all()
    df = pd.DataFrame(data)

    if df.empty:
        st.info("No data yet")
        return

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Items", len(df))
    col2.metric("Unique Barcodes", df["barcode"].nunique())
    col3.metric("Item Types", df["item_name"].nunique())

    st.divider()
    st.dataframe(df, use_container_width=True)

# ---------------- SCANNER ----------------
def scanner():
    st.subheader("📦 Scan Item")

    if "last_barcode" not in st.session_state:
        st.session_state.last_barcode = ""

    barcode = st.text_input("Scan Barcode")
    item_name = st.text_input("Item Name")

    if barcode and barcode != st.session_state.last_barcode:
        add_item(barcode, item_name if item_name else "Unknown")
        st.session_state.last_barcode = barcode
        st.success(f"Saved: {barcode}")

# ---------------- MAIN ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login()
else:
    header()

    st.sidebar.image("logo.png", width=100)
    st.sidebar.markdown("### Inventory System")
    st.sidebar.caption("Sweetson Joseph")

    menu = st.sidebar.radio("Navigation", ["Dashboard", "Scan Item"])

    if menu == "Dashboard":
        dashboard()
    elif menu == "Scan Item":
        scanner()

    st.divider()
    st.caption("© 2026 Sweetson Joseph")
