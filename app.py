import streamlit as st
from datetime import datetime
import hashlib
import requests
from supabase import create_client, Client

# Supabase setup
SUPABASE_URL = "https://qkuwfmqtwrlxmztxcvmc.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFrdXdmbXF0d3JseG16dHhjdm1jIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTExOTY5NTEsImV4cCI6MjA2Njc3Mjk1MX0.JHwF3hgV5GdaNHt0ViLMg4F_KUlK0ZtCjeM78e5bPZ4"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- LOVE LOGIC ---
def love_score(name1, name2):
    combined = (name1 + name2).lower()
    count = sum(combined.count(ch) for ch in "love")
    score = (count * 42) % 101
    return score

# --- Save to Supabase ---
def save_to_supabase(name1, name2, score, location):
    data = {
        "name1": name1,
        "name2": name2,
        "score": score,
        "created_at": datetime.now().isoformat(),
        "location": location,
    }
    supabase.table("love_results").insert(data).execute()

# --- Get user location ---
def get_location():
    try:
        res = requests.get("https://ipinfo.io/json").json()
        return res.get("city", "Unknown") + ", " + res.get("region", "")
    except:
        return "Unknown"

# --- UI ---
st.set_page_config(page_title="❤ Love Calculator", layout="centered")

with st.container():
    st.markdown("""
        <style>
            .title { text-align: center; font-size: 36px; font-weight: bold; }
            .score { font-size: 48px; text-align: center; margin-top: 20px; }
            .result { font-size: 22px; text-align: center; margin-top: 10px; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="title">💘 Love Calculator</div>', unsafe_allow_html=True)

    name1 = st.text_input("Your Name", max_chars=20)
    name2 = st.text_input("Crush's Name", max_chars=20)

    if st.button("Calculate ❤"):
        if name1 and name2:
            score = love_score(name1, name2)
            location = get_location()
            save_to_supabase(name1, name2, score, location)

            st.markdown(f'<div class="score">{score}% ❤</div>', unsafe_allow_html=True)
            if score > 80:
                st.success("You're a perfect match! 💑💍")
            elif score > 50:
                st.info("There's definitely a spark! ✨")
            else:
                st.warning("You might want to stay friends 😅")
        else:
            st.error("Please enter both names.")

# Optional: Show past results
with st.expander("📜 View Past Results"):
    result = supabase.table("love_results").select("*").order("created_at", desc=True).limit(5).execute()
    for row in result.data:
        st.write(f"{row['name1']} ❤ {row['name2']} — {row['score']}% — {row['location']} on {row['created_at']}")
