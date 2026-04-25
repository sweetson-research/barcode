import streamlit as st
from supabase import create_client

@st.cache_resource
def get_client():
    return create_client(
        st.secrets["supabase"]["url"],
        st.secrets["supabase"]["key"]
    )

def add_item(barcode, name):
    get_client().table("items").insert({
        "barcode": barcode,
        "item_name": name
    }).execute()

def get_all():
    res = get_client().table("items").select("*").order("created_at", desc=True).execute()
    return res.data