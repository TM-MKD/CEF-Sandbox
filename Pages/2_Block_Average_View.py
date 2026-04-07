import streamlit as st
import pandas as pd
from reportlab.lib import colors

# ===================== PAGE CONFIG =====================
st.set_page_config(
    page_title="MK Dons – Block Average",
    layout="wide"
)

# ===================== HEADER =====================
col1, col2 = st.columns([1, 6])

with col1:
    try:
        st.image("assets/mkdons_badge.png", width=90)
    except:
        pass

with col2:
    st.markdown(
        "<h1 style='margin-bottom:0;'>MK Dons – Block Average View</h1>",
        unsafe_allow_html=True
    )

st.markdown("---")

# ===================== CONSTANTS =====================
GROUP_LABELS = [
    "Understanding Self",
    "Coaching Individuals",
    "Coaching Practice",
    "Skill Acquisition",
    "MK Dons",
    "Psychology/Social Support",
    "Relationships",
    "Athletic Development",
    "Wellbeing/Lifestyle"
]

SAFEGUARDING_QUESTIONS = [
    "Are you aware of the clubs safeguarding policies?",
    "Can you notice changes in child behaviour?",
    "Do you signpost players to appropriate support?",
    "Can you use Myconcern to report safeguarding concerns and follow up where/when appropriate?",
    "Are you comfortable checking (and where necessary) challenging poor practice?"
]

score_map = {
    "YES": 1,
    "Neither YES or NO": 0.5,
    "NO": 0
}

# ===================== HELPERS =====================
def get_group_colour(score):
    if score >= 3.25:
        return "#4CAF50"
    elif score >= 2.51:
        return "#FFD966"
    elif score >= 1.75:
        return "#F4A261"
    else:
        return "#FF6B6B"


def get_safeguarding_colour(score):
    if score >= 0.8:
        return "#4CAF50"
    elif score >= 0.5:
        return "#F4A261"
    else:
        return "#FF6B6B"


def calculate_average_group_totals(block_df, question_cols):
    averages = []

    for i in range(0, len(question_cols), 4):
        cols = question_cols[i:i+4]

        group_scores = block_df[cols].apply(
            pd.to_numeric, errors="coerce"
        )

        row_totals = group_scores.sum(axis=1)

        averages.append(round(row_totals.mean(), 2))

    return averages


def make_group_grid(group_totals):
    cols = st.columns(3)

    for idx, (label, score) in enumerate(zip(GROUP_LABELS, group_totals)):
        with cols[idx % 3]:
            st.markdown(
                f"""
                <div style="
                    background-color:{get_group_colour(score)};
                    padding:18px;
                    border-radius:10px;
                    text-align:center;
                    margin-bottom:10px;
                    box-shadow:0 4px 10px rgba(0,0,0,0.15);
                ">
                    <div style="font-size:26px;font-weight:bold;">{score}</div>
                    <div style="font-size:12px;">{label}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

# ===================== FILE UPLOAD =====================
uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])

if uploaded_file is None:
    st.info("Please upload an Excel file to begin.")
    st.stop()

# ===================== LOAD DATA =====================
df = pd.read_excel(uploaded_file)
df.columns = df.columns.str.strip()

question_cols = [
    col for col in df.columns
    if col not in ["Full Name"]
]

for col in question_cols:
    df[col] = df[col].map(score_map)

df["Block_Number"] = df.groupby("Full Name").cumcount() + 1
df["Block_Name"] = "Block " + df["Block_Number"].astype(str)

blocks = {}

for block_name in sorted(df["Block_Name"].unique()):
    blocks[block_name] = df[df["Block_Name"] == block_name].reset_index(drop=True)

# ===================== BLOCK SELECTION =====================
block_selected = st.selectbox(
    "Select Block",
    options=list(blocks.keys()),
    index=None
)

if block_selected is None:
    st.info("Please select a block.")
    st.stop()

block_df = blocks[block_selected]

# ===================== CEF BREAKDOWN =====================
st.markdown("---")
st.subheader("Average CEF Breakdown")

group_totals = calculate_average_group_totals(block_df, question_cols)
cef_total = round(sum(group_totals), 2)

st.markdown(f"### Average Score: **{cef_total} / 36**")

make_group_grid(group_totals)

# ===================== SAFEGUARDING =====================
st.markdown("---")
st.subheader("Average Safeguarding")

safe_scores = []

for q in SAFEGUARDING_QUESTIONS:
    avg_score = round(pd.to_numeric(block_df[q], errors="coerce").mean(), 2)
    safe_scores.append(avg_score)

safe_total = round(sum(safe_scores), 2)

st.markdown(f"### Average Score: **{safe_total} / 5**")

cols = st.columns(5)

for col, q, score in zip(cols, SAFEGUARDING_QUESTIONS, safe_scores):
    with col:
        st.markdown(
            f"""
            <div style="
                background-color:{get_safeguarding_colour(score)};
                padding:16px;
                border-radius:12px;
                text-align:center;
                height:130px;
                box-shadow:0 4px 10px rgba(0,0,0,0.15);
            ">
                <div style="font-size:26px;font-weight:bold;">{score}</div>
                <div style="font-size:11px;margin-top:6px;">
                    {q}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# ===================== ACTION PLAN =====================
st.markdown("---")
st.subheader("Team Development Areas")

improve = []
attention = []

for col in question_cols:
    avg_score = round(pd.to_numeric(block_df[col], errors="coerce").mean(), 2)

    if avg_score <= 0.5:
        attention.append(col)
    elif avg_score <= 0.75:
        improve.append(col)

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Consider Improving")
    for item in improve:
        st.write(item)

with col2:
    st.markdown("#### Immediate Attention Needed")
    for item in attention:
        st.write(item)
