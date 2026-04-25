import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

SCOPE = ["https://www.googleapis.com/auth/spreadsheets"]

@st.cache_resource
def connect_sheet():
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=SCOPE
    )
    client = gspread.authorize(creds)
    sheet = client.open_by_key(st.secrets["gcp_service_account"]["sheet_id"])
    return sheet.sheet1

def add_item(barcode, name, timestamp):
    connect_sheet().append_row([barcode, name, timestamp])

def get_all():
    return connect_sheet().get_all_records()