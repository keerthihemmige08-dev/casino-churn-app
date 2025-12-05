import streamlit as st
import pandas as pd
import joblib
import os

# ---------------- Page Config ----------------
st.set_page_config(page_title="Casino Churn Predictor", layout="centered")

# ---------------- Paths ----------------
# Get the directory where app.py is located
BASE_DIR = os.path.dirname(__file__)

# ---------------- Load Model ----------------
model = joblib.load(os.path.join(BASE_DIR, 'casino_churn_model.pkl'))
label_encoders = joblib.load(os.path.join(BASE_DIR, 'label_encoders.pkl'))
feature_columns = joblib.load(os.path.join(BASE_DIR, 'feature_columns.pkl'))

model = joblib.load(model_path)
label_encoders = joblib.load(encoders_path)
feature_columns = joblib.load(features_path)

# ---------------- Dark Theme Colors ----------------
bg_color = "#0b0c10"
card_bg = "rgba(20, 20, 20, 0.85)"
text_color = "#f0f0f0"
border_color = "#ff5722"
button_bg = "#1f1f1f"
button_hover = "#ff5722"
box_good = "#1b5e20"
box_bad = "#c62828"

# ---------------- CSS ----------------
st.markdown(f"""
<style>
body {{
    margin:0;
    padding:0;
    background: {bg_color};
    overflow-x:hidden;
}}
/* Floating casino elements */
.casino-icon {{
    position: fixed;
    font-size: 28px;
    opacity: 0.15;
    animation-name: floatUpDown;
    animation-iteration-count: infinite;
    animation-timing-function: linear;
}}
@keyframes floatUpDown {{
    0% {{transform: translateY(100vh) rotate(0deg);}}
    50% {{transform: translateY(-20vh) rotate(180deg);}}
    100% {{transform: translateY(100vh) rotate(360deg);}}
}}
/* Glassmorphic input card */
.card {{
    background: {card_bg};
    padding: 30px;
    border-radius: 25px;
    border: 2px solid rgba(255, 87, 34, 0.6);
    box-shadow: 0 10px 25px rgba(0,0,0,0.45), 0 0 30px rgba(255,87,34,0.2);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    animation: neonPulse 2.5s infinite alternate;
}}
@keyframes neonPulse {{
    from {{ box-shadow: 0 10px 25px rgba(0,0,0,0.45), 0 0 15px rgba(255,87,34,0.3); }}
    to {{ box-shadow: 0 10px 25px rgba(0,0,0,0.45), 0 0 30px rgba(255,87,34,0.6); }}
}}
/* Buttons */
.stButton>button {{
    width: 100%;
    background: {button_bg};
    border: none;
    border-radius: 16px;
    color: white;
    font-size: 18px;
    padding: 14px 0;
    cursor: pointer;
    transition: 0.2s ease-in-out;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}}
.stButton>button:hover {{
    background: {button_hover};
    transform: translateY(-2px);
    box-shadow: 0 6px 18px rgba(0,0,0,0.4);
}}
/* Prediction Box */
.predict-box {{
    padding: 20px;
    font-size: 22px;
    border-radius: 16px;
    font-weight: 600;
    text-align: center;
    margin-top: 15px;
    animation: slideUp 0.6s ease-out;
    box-shadow: 0 8px 20px rgba(0,0,0,0.35);
}}
.predict-leave {{
    background: linear-gradient(135deg, #ffcccc, #ff9999);
    color: #b71c1c;
    border: 2px solid #ff8a80;
}}
.predict-stay {{
    background: linear-gradient(135deg, #ccffcc, #99ff99);
    color: #1b5e20;
    border: 2px solid #81c784;
}}
@keyframes slideUp {{
    from {{ transform: translateY(20px); opacity: 0; }}
    to {{ transform: translateY(0); opacity: 1; }}
}}
/* Inputs */
input, select {{
    border-radius: 12px !important;
    border: 2px solid rgba(255,255,255,0.2) !important;
    padding: 8px;
    font-weight: 500;
    background: rgba(0,0,0,0.1);
    color: {text_color};
    transition: all 0.3s ease;
}}
input:focus, select:focus {{
    border-color: {border_color} !important;
    box-shadow: 0 0 12px {border_color};
}}
/* Footer */
.footer {{
    margin-top: 40px;
    text-align: center;
    font-size: 14px;
    color: {text_color};
    opacity: 0.7;
}}
</style>

<!-- Floating casino icons -->
<div class="casino-icon" style="left:5%; animation-duration:22s;">🎲</div>
<div class="casino-icon" style="left:15%; animation-duration:24s;">🎰</div>
<div class="casino-icon" style="left:30%; animation-duration:23s;">🃏</div>
<div class="casino-icon" style="left:45%; animation-duration:26s;">♠️</div>
<div class="casino-icon" style="left:60%; animation-duration:25s;">♥️</div>
<div class="casino-icon" style="left:75%; animation-duration:28s;">💎</div>
<div class="casino-icon" style="left:85%; animation-duration:20s;">🤑</div>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown(f"<h1 style='text-align:center; color:{text_color};'>🎰 Casino Churn Predictor</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; color:{text_color}; opacity:0.85;'>Predict if a player will stay or leave the casino.</p>", unsafe_allow_html=True)

# ---------------- INPUT FORM ----------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    age = st.number_input("🎂 Age", 10, 100, 25)
    gender = st.selectbox("👤 Gender", ["Male", "Female"])
    playtime_hours = st.number_input("🕹 Weekly Playtime Hours", 0.0, 50.0, 5.0)
    in_game_purchases = st.selectbox("💰 In-game purchases?", ["No", "Yes"])
    game_difficulty = st.selectbox("🎮 Difficulty", ["Easy", "Medium", "Hard"])
with col2:
    sessions_per_week = st.number_input("📅 Sessions per week", 0, 20, 3)
    avg_session_duration_hours = st.number_input("⏱ Avg session duration (hours)", 0.0, 24.0, 1.0)
    avg_session_duration = avg_session_duration_hours * 60
    player_level = st.number_input("🏆 Player level", 1, 100, 1)
    achievements_unlocked = st.number_input("🎖 Achievements unlocked", 0, 100, 0)
st.markdown("</div>", unsafe_allow_html=True)

# ---------------- PREPROCESS ----------------
input_dict = {
    "Age": age,
    "Gender": gender,
    "PlayTimeHours": playtime_hours,
    "InGamePurchases": in_game_purchases,
    "GameDifficulty": game_difficulty,
    "SessionsPerWeek": sessions_per_week,
    "AvgSessionDurationMinutes": avg_session_duration,
    "PlayerLevel": player_level,
    "AchievementsUnlocked": achievements_unlocked,
}
input_df = pd.DataFrame([input_dict])
for col, enc in label_encoders.items():
    if col in input_df:
        try:
            input_df[col] = enc.transform(input_df[col])
        except:
            input_df[col] = enc.transform([enc.classes_[0]])[0]
fallback = {
    "Gender": {"Male": 0, "Female": 1},
    "InGamePurchases": {"No": 0, "Yes": 1},
    "GameDifficulty": {"Easy": 0, "Medium": 1, "Hard": 2},
}
for col, mp in fallback.items():
    if input_df[col].dtype == "object":
        input_df[col] = input_df[col].map(mp)
input_df = input_df.reindex(columns=feature_columns, fill_value=0)

# ---------------- PREDICT ----------------
if st.button("Predict", use_container_width=True):
    prob = model.predict_proba(input_df)[0][1]
    pred = 1 if prob > 0.5 else 0
    if pred == 1:
        st.markdown(f"<div class='predict-box predict-leave'>⚠ Player Likely to Leave</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='predict-box predict-stay'>✔ Player Likely to Stay</div>", unsafe_allow_html=True)
    st.subheader("📊 Churn Probability")
    st.progress(float(prob))
    st.write(f"**Probability of Leaving:** `{prob:.2f}`")
    st.write(f"**Probability of Staying:** `{1 - prob:.2f}`")

# ---------------- FOOTER ----------------
st.markdown(f"<div class='footer'>🎰 Professional Casino Dashboard </div>", unsafe_allow_html=True)
