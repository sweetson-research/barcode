import streamlit as st

from datetime import datetime

from sheets import add_item, get_all

import pandas as pd



# ---------------- CONFIG ----------------

st.set_page_config(page_title="Inventory", layout="wide")



# ---------------- MODERN MINIMAL CSS ----------------

st.markdown("""

<style>

/* App background */

.main {

    background-color: #fafafa;

}



/* Sidebar */

section[data-testid="stSidebar"] {

    background-color: #ffffff;

    border-right: 1px solid #e5e7eb;

}



/* Cards */

.card {

    padding: 18px;

    border-radius: 12px;

    background: white;

    border: 1px solid #e5e7eb;

}



/* Metric */

.metric {

    font-size: 28px;

    font-weight: 600;

}

.metric-label {

    color: #6b7280;

    font-size: 14px;

}



/* Buttons */

.stButton>button {

    border-radius: 8px;

    background: #111827;

    color: white;

    border: none;

    padding: 0.4rem 1rem;

}



/* Inputs */

input {

    border-radius: 8px !important;

}



/* Header */

.header-title {

    font-size: 22px;

    font-weight: 600;

}

.subtle {

    color: #6b7280;

    font-size: 13px;

}

</style>

""", unsafe_allow_html=True)



# ---------------- LOGIN ----------------

def login():

    st.markdown("## Sign in")



    col1, col2, col3 = st.columns([1,2,1])

    with col2:

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

    st.markdown("""

    <div>

        <div class="header-title">Inventory</div>

        <div class="subtle">Developed by Sweetson Joseph</div>

    </div>

    """, unsafe_allow_html=True)



# ---------------- DASHBOARD ----------------

def dashboard():

    data = get_all()

    df = pd.DataFrame(data)



    st.markdown("### Overview")



    if df.empty:

        st.info("No data yet")

        return



    col1, col2, col3 = st.columns(3)



    with col1:

        st.markdown(f"""

        <div class="card">

            <div class="metric">{len(df)}</div>

            <div class="metric-label">Total Items</div>

        </div>

        """, unsafe_allow_html=True)



    with col2:

        st.markdown(f"""

        <div class="card">

            <div class="metric">{df["barcode"].nunique()}</div>

            <div class="metric-label">Unique Barcodes</div>

        </div>

        """, unsafe_allow_html=True)



    with col3:

        st.markdown(f"""

        <div class="card">

            <div class="metric">{df["item_name"].nunique()}</div>

            <div class="metric-label">Item Types</div>

        </div>

        """, unsafe_allow_html=True)



    st.markdown("### Items")



    st.dataframe(df, use_container_width=True)



# ---------------- SCANNER ----------------

def scanner():

    st.markdown("### Scan item")



    col1, col2 = st.columns([2,2])



    with col1:

        barcode = st.text_input("Barcode", key="barcode")



    with col2:

        item_name = st.text_input("Item name")



    if barcode:

        add_item(

            barcode,

            item_name if item_name else "Unknown",

            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

        )

        st.success(f"Saved {barcode}")

        st.session_state.barcode = ""

        st.rerun()



# ---------------- MAIN ----------------

if "logged_in" not in st.session_state:

    st.session_state.logged_in = False



if not st.session_state.logged_in:

    login()

else:

    header()



    st.sidebar.markdown("### Inventory")

    st.sidebar.caption("Sweetson Joseph")



    menu = st.sidebar.radio("", ["Dashboard", "Scan"])



    if menu == "Dashboard":

        dashboard()

    elif menu == "Scan":

        scanner()



    st.markdown("---")

    st.caption("© 2026 Sweetson Joseph")