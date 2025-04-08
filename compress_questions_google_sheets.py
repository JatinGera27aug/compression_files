import streamlit as st
import zlib
import base64
from datetime import datetime
import gspread
import json
from google.oauth2.service_account import Credentials



# Page setup
st.set_page_config(page_title="Compress Your Questions", layout="centered", page_icon="🗜️")

# Dark mode CSS
st.markdown(
    """
    <style>
    body, .stApp {
        background-color: #121212;
        color: white;
    }
    .css-1aumxhk {
        background-color: #1f1f1f;
    }
    .stTextArea, .stTextInput {
        background-color: #1e1e1e !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True
)

# Title
st.markdown("<h1 style='text-align: center;'>Compress Your Questions, Not Your Curiosity</h1>", unsafe_allow_html=True)


# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = st.secrets["google_service_account"]
creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
client = gspread.authorize(creds)


# Open your sheet (REPLACE name with your sheet name)
sheet = client.open("Compressed Questions Log").sheet1

# User input
user_input = st.text_area("Enter your question below:", height=150)

if user_input:
    # Compression
    compressed = zlib.compress(user_input.encode())
    compressed_b64 = base64.b64encode(compressed).decode()
    decompressed = zlib.decompress(base64.b64decode(compressed_b64)).decode()

    # Stats
    original_size = len(user_input.encode())
    compressed_size = len(compressed)
    savings = round(((original_size - compressed_size) / original_size) * 100, 2)

    # Display
    st.subheader("📦 Compressed Message (Base64)")
    st.code(compressed_b64)

    st.subheader("🔄 Decompressed Message")
    st.success(decompressed)

    st.subheader("📊 Compression Stats")
    st.markdown(f"**Original Size:** {original_size} bytes")
    st.markdown(f"**Compressed Size:** {compressed_size} bytes")
    st.markdown(f"**Space Saved:** {savings}%")

    # Log to Google Sheet
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([timestamp, user_input, compressed_b64, f"{savings}%"])
    st.success("✅ Question saved to shared log successfully!")
