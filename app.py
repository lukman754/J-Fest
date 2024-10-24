import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import threading
import time
import pandas as pd

# Konfigurasi kredensial Google API
scope = ["https://www.googleapis.com/auth/spreadsheets", 
         "https://www.googleapis.com/auth/drive"]
creds, _ = Credentials.from_authorized_user_info({}, scope)
gc = gspread.authorize(creds)

# URL spreadsheet
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1RQ2PZMRKjBVHpG0ettmuiDjjxzpF7OfFDfXlJDT0ElE/edit?usp=drivesdk"

# Fungsi untuk membaca data dari Google Sheets
def fetch_data():
    sh = gc.open_by_url(SPREADSHEET_URL)
    worksheet = sh.get_worksheet(0)
    data = worksheet.get_all_values()
    df = pd.DataFrame(data[1:], columns=data[0])  # Konversi ke DataFrame
    return df

# Fungsi untuk memperbarui data secara berkala (real-time)
def update_data():
    while True:
        with data_lock:
            st.session_state['data'] = fetch_data()
        time.sleep(10)  # Update setiap 10 detik

# Kunci untuk menghindari konflik data saat threading
data_lock = threading.Lock()

# Inisialisasi data saat pertama kali dijalankan
if 'data' not in st.session_state:
    st.session_state['data'] = fetch_data()

# Mulai thread untuk memperbarui data
if 'update_thread' not in st.session_state:
    update_thread = threading.Thread(target=update_data, daemon=True)
    update_thread.start()
    st.session_state['update_thread'] = update_thread

# Tampilan di Streamlit
st.title("Dashboard Google Sheets (Real-Time)")

with data_lock:
    df = st.session_state['data']

st.dataframe(df)
