import streamlit as st
import pandas as pd
from datetime import datetime
from sheets import add_item, get_all

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Inventory System", layout="wide")

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

# ---------------- DASHBOARD ----------------
def dashboard():
    st.header("📊 Dashboard")

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
    st.header("📦 Scan Item")

    barcode = st.text_input("Scan Barcode", key="barcode")
    item_name = st.text_input("Item Name")

    if barcode:
        add_item(
            barcode,
            item_name if item_name else "Unknown",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        st.success(f"Saved: {barcode}")
        st.session_state.barcode = ""
        st.rerun()

# ---------------- MAIN ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login()
else:
    st.title("📦 Inventory Management System")
    st.caption("Developed by Sweetson Joseph")

    menu = st.sidebar.radio("Navigation", ["Dashboard", "Scan Item"])

    if menu == "Dashboard":
        dashboard()
    elif menu == "Scan Item":
        scanner()

    st.divider()
    st.caption("© 2026 Sweetson Joseph")