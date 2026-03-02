import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import pagesizes
from reportlab.lib.units import inch
from io import BytesIO


# ===================== PAGE CONFIG =====================
st.set_page_config(
    page_title="MK Dons – CEF SANDBOX",
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
        "<h1 style='margin-bottom:0;'>MK Dons – CEF SANDBOX</h1>",
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

SAFEGUARDING_QUESTIONS = [22, 20, 30, 33, 34]


# ---------- Excel Header Mapping ----------
CEF_QUESTIONS = {
    "Q1": "Do you understand your role?",
    "Q2": "Do you engage with club coach CPD?",
    "Q3": "Do you communicate effectively?",
    "Q4": "Do you engage with players and parents informally?",
    "Q5": "Do you understand the game model?",
    "Q6": "Do you seek to understand decisions?",
    "Q7": "Are you positive and inspiring?",
    "Q8": "Do you set realistic goals for players?",
    "Q9": "Do you use appropriate interventions?",
    "Q10": "Do you understand player differences?",
    "Q11": "Do you understand and apply LTPD?",
    "Q12": "Do you support coaching with video and data?",
    "Q13": "Do you introduce sessions effectively?",
    "Q14": "Do you embed deliberate practice?",
    "Q15": "Do you create action plans for players?",
    "Q16": "Do you debrief sessions?",
    "Q17": "Do you use club coaching methodology?",
    "Q18": "Do you adopt club principles (H-O-P)?",
    "Q19": "Do you adopt a multi-disciplinary approach?",
    "Q20": "Are you aware of safeguarding policies and procedures?",
    "Q21": "Do you embed competencies each session?",
    "Q22": "Do you notice changes in a child's behaviour?",
    "Q23": "Do you signpost players to appropriate support?",
    "Q24": "Are you a critical thinker who checks and challenges?",
    "Q25": "Do you manage other staff supporting sessions?",
    "Q26": "Do you listen and suspend judgement?",
    "Q27": "Do you have a recognised coaching cell in the club?",
    "Q28": "Do you watch other coaches inside the club?",
    "Q29": "Do you embed physical development?",
    "Q30": "Do you make practice competitive and realistic?",
    "Q31": "Do you develop players physically through session design?",
    "Q32": "Do you drive intensity using coaching strategies?",
    "Q33": "Do you report issues using MyConcern appropriately?",
    "Q34": "Are you comfortable challenging poor practice?",
    "Q35": "Are you an ambassador of MK Dons?",
    "Q36": "Do you have clear interests away from coaching?"
}


# ---------- Action Plan Text (unchanged) ----------
QUESTION_TEXT = {i: CEF_QUESTIONS[f"Q{i}"] for i in range(1, 37)}


# ===================== COLOUR HELPERS =====================
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
    if score == 1:
        return "#4CAF50"
    elif score == 0.5:
        return "#F4A261"
    else:
        return "#FF6B6B"


def calculate_group_totals(person_data, ordered_questions):
    totals = []
    for i in range(0, len(ordered_questions), 4):
        group = ordered_questions[i:i+4]
        totals.append(round(sum(person_data[q] for q in group), 2))
    return totals


def make_group_grid(group_totals):
    cols = st.columns(3)
    for idx, (label, score) in enumerate(zip(GROUP_LABELS, group_totals)):
        with cols[idx % 3]:
            st.markdown(
                f"""
                <div style="
                    background-color:{get_group_colour(score)};
                    padding:18px;
                    border-radius:12px;
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


# ===================== PARSE SINGLE TABLE =====================
df = pd.read_excel(uploaded_file)
df.columns = df.columns.str.strip()

score_map = {"YES": 1, "Neither YES or NO": 0.5, "NO": 0}

question_columns = [v for v in CEF_QUESTIONS.values() if v in df.columns]

for col in question_columns:
    df[col] = df[col].map(score_map)

df["Block_Number"] = df.groupby("Full Name").cumcount() + 1
df["Block_Name"] = "Block " + df["Block_Number"].astype(str)

blocks = {}
for block in sorted(df["Block_Name"].unique()):
    blocks[block] = df[df["Block_Name"] == block].reset_index(drop=True)


# ===================== SELECTIONS =====================
coach = st.selectbox(
    "Select Coach",
    options=sorted(df["Full Name"].unique()),
    index=None,
    placeholder="Select a coach"
)

block_selected = st.selectbox(
    "Select Block",
    options=list(blocks.keys()),
    index=None,
    placeholder="Select a block"
)

if coach is None or block_selected is None:
    st.info("Please select a coach and a block.")
    st.stop()

df_block = blocks[block_selected]

if coach not in df_block["Full Name"].values:
    st.warning("Coach did not complete this block.")
    st.stop()

person_data = df_block[df_block["Full Name"] == coach].iloc[0]


# ===================== CEF BREAKDOWN =====================
st.markdown("---")
st.subheader("CEF Breakdown")

ordered_questions = [CEF_QUESTIONS[f"Q{i}"] for i in range(1, 37)]
group_totals = calculate_group_totals(person_data, ordered_questions)
cef_total = round(sum(group_totals), 2)

st.markdown(f"### Score: **{cef_total} / 36**")
make_group_grid(group_totals)


# ===================== SAFEGUARDING =====================
st.markdown("---")
st.subheader("Safeguarding")

safeguarding_scores = [
    person_data[CEF_QUESTIONS[f"Q{q}"]]
    for q in SAFEGUARDING_QUESTIONS
]

safeguarding_total = sum(safeguarding_scores)

st.markdown(f"### Score: **{safeguarding_total} / 5**")

cols = st.columns(5)
for col, q in zip(cols, SAFEGUARDING_QUESTIONS):
    score = person_data[CEF_QUESTIONS[f"Q{q}"]]
    with col:
        st.markdown(
            f"""
            <div style="
                background-color:{get_safeguarding_colour(score)};
                padding:16px;
                border-radius:10px;
                text-align:center;
                height:120px;
                box-shadow:0 4px 10px rgba(0,0,0,0.15);
            ">
                <div style="font-size:11px;font-weight:bold;">Q{q}</div>
                <div style="font-size:10px;margin-top:6px;">
                    {QUESTION_TEXT[q]}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


# ===================== ACTION PLAN =====================
st.markdown("---")
st.subheader("Action Plan")

half_scores, zero_scores = [], []

for i in range(1, 37):
    q_code = f"Q{i}"
    q_text = CEF_QUESTIONS[q_code]
    score = person_data[q_text]

    if score == 0.5:
        half_scores.append(f"{q_code} – {QUESTION_TEXT[i]}")
    elif score == 0:
        zero_scores.append(f"{q_code} – {QUESTION_TEXT[i]}")

c1, c2 = st.columns(2)

with c1:
    st.subheader("Scored 0.5 (Developing)")
    for item in half_scores:
        st.write("•", item)

with c2:
    st.subheader("Scored 0 (Needs Attention)")
    for item in zero_scores:
        st.write("•", item)


# ===================== BAR CHART =====================
scores = [person_data[CEF_QUESTIONS[f"Q{i}"]] for i in range(1, 37)]

bar_colors = [
    "#4CAF50" if s == 1 else "#F4A261" if s == 0.5 else "#FF6B6B"
    for s in scores
]

fig = go.Figure()
fig.add_trace(go.Bar(
    x=[f"Q{i}" for i in range(1, 37)],
    y=scores,
    marker_color=bar_colors
))

fig.update_layout(
    title=f"{coach} — {block_selected}",
    yaxis=dict(range=[0, 1]),
    xaxis_title="Questions",
    yaxis_title="Score"
)

st.plotly_chart(fig, use_container_width=True)
