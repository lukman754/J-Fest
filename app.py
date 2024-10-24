import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import json
import os

# Simpan kredensial ke file credentials.json
with open("credentials.json", "w") as f:
    f.write(st.secrets["GCP_CREDENTIALS"])

# Konfigurasi kredensial Google API
scope = ["https://www.googleapis.com/auth/spreadsheets", 
         "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file("credentials.json", scopes=scope)
gc = gspread.authorize(creds)

# URL spreadsheet
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1RQ2PZMRKjBVHpG0ettmuiDjjxzpF7OfFDfXlJDT0ElE/edit?usp=drivesdk"

# Fungsi untuk membaca data dari Google Sheets
@st.cache_data(ttl=600)  # Cache data selama 10 menit
def fetch_data():
    sh = gc.open_by_url(SPREADSHEET_URL)
    worksheet = sh.get_worksheet(0)
    data = worksheet.get_all_values()
    df = pd.DataFrame(data[1:], columns=data[0])
    return df

# Judul aplikasi
st.title("Dashboard Google Sheets (Real-Time)")

# Tampilkan data dalam bentuk tabel
df = fetch_data()
st.dataframe(df)

# Informasi pembaruan terakhir
st.caption(f"Terakhir diperbarui: {pd.Timestamp.now()}")
