import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import pagesizes
from reportlab.lib.units import inch
from io import BytesIO


# ===================== PAGE CONFIG =====================
st.set_page_config(
    page_title="MK Dons – CEF Sandbox",
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
        "<h1 style='margin-bottom:0;'>MK Dons – CEF Sandbox</h1>",
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

# ===================== DATA HELPERS =====================

def calculate_group_totals(person_data, question_cols):

    totals = []

    for i in range(0, len(question_cols), 4):
        cols = question_cols[i:i+4]

        scores = pd.to_numeric(person_data[cols], errors="coerce")

        totals.append(round(scores.sum(), 2))

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

score_map = {
    "YES": 1,
    "Neither YES or NO": 0.5,
    "NO": 0
}

question_cols = [
    "Do you Understand your role?",
    "Do you Engage with Club CPD?",
    "Do you Communicate Effectively?",
    "Do you engage with players at all times and also with parents informally around training and match day?",
    "Do you Understand the game model?",
    "Do you seek to understand others decisions through questions",
    "Do you inspire people and act positively?",
    "Do you set realistic goals for players?",
    "Do you use appropriate interventions when coaching?",
    "Do you understand player differences?",
    "Do you Understand and apply LTPD?",
    "Do you support your coaching with video and data?",
    "Do you introduce each session to players?",
    "Do you embed deliberate practice into sessions?",
    "Do you create action plans for players?",
    "Do you Debrief sessions and fixtures? (with the group and then via FiP)",
    "Do you use the club coaching methodology?",
    "Do you adopt the Academy principles (HOP)",
    "Do you adopt a multi-disciplinary approach?",
    "Are you aware of the clubs safeguarding policies?",
    "Do you embed Competencies into each session?",
    "Can you notice changes in child behaviour?",
    "Do you signpost players to appropriate support?",
    "Do you critically think and challenge where necessary?",
    "Do you manage other staff effectively to assist with the delivery of coaching sessions?",
    "Do you listen and suspend judgement when talking with players?",
    "Do you have a recognised/established coaching cell in the club?",
    "Do you watch other coaches inside the football club?",
    "Do you embed physical development in sessions?",
    "Do you make sessions competitive and realistic?",
    "Do you demonstrate the ability to develop players physically through session design?",
    "Do you drive intensity in training through a variety of coaching interventions/strategies?",
    "Can you use Myconcern to report safeguarding concerns and follow up where/when appropriate?",
    "Are you comfortable checking (and where necessary) challenging poor practice?",
    "Do you have clear interests away from the club that others know about?",
    "Do you embrace MK Dons as your club and act as an ambassador for the club?"
]

question_cols = [c for c in df.columns if c in question_cols]

for col in question_cols:
    df[col] = df[col].map(score_map)

df["Block_Number"] = df.groupby("Full Name").cumcount() + 1
df["Block_Name"] = "Block " + df["Block_Number"].astype(str)

blocks = {}

for block_name in sorted(df["Block_Name"].unique()):
    blocks[block_name] = df[df["Block_Name"] == block_name].reset_index(drop=True)

# ===================== SELECTIONS =====================

first_block = next(iter(blocks.values()))

coach = st.selectbox(
    "Select Coach",
    options=first_block["Full Name"],
    index=None
)

block_selected = st.selectbox(
    "Select Block",
    options=list(blocks.keys()),
    index=None
)

if coach is None or block_selected is None:
    st.info("Please select a coach and a block to view results.")
    st.stop()

df = blocks[block_selected]
person_data = df[df["Full Name"] == coach].iloc[0]

# ===================== CEF BREAKDOWN =====================

st.markdown("---")
st.subheader("CEF Breakdown")

group_totals = calculate_group_totals(person_data, question_cols)
cef_total = round(sum(group_totals), 2)

st.markdown(f"### Score: **{cef_total} / 36**")

make_group_grid(group_totals)

# ===================== SAFEGUARDING =====================

st.markdown("---")
st.subheader("Safeguarding")

safeguarding_scores = [
    pd.to_numeric(person_data[q], errors="coerce")
    for q in SAFEGUARDING_QUESTIONS
]

safeguarding_total = sum(safeguarding_scores)

st.markdown(f"### Score: **{safeguarding_total} / 5**")

cols = st.columns(5)

for col, q in zip(cols, SAFEGUARDING_QUESTIONS):

    score = pd.to_numeric(person_data[q], errors="coerce")

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
st.subheader("Action Plan")

half_scores, zero_scores = [], []

for i, q_col in enumerate(question_cols, start=1):

    score = pd.to_numeric(person_data[q_col], errors="coerce")

    if score == 0.5:
        half_scores.append(f"Q{i} – {q_col}")

    elif score == 0:
        zero_scores.append(f"Q{i} – {q_col}")

if half_scores:

    st.markdown("#### Consider Improving")

    for item in half_scores:
        st.write(item)

if zero_scores:

    st.markdown("#### Immediate Attention Needed")

    for item in zero_scores:
        st.write(item)

# ===================== PDF GENERATION =====================

def generate_pdf():

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=pagesizes.A4
    )

    elements = []

    styles = getSampleStyleSheet()

    elements.append(Paragraph("MK Dons – Coach Evaluation Report", styles["Title"]))

    elements.append(Spacer(1,20))

    elements.append(Paragraph(f"Coach: {coach}", styles["Normal"]))
    elements.append(Paragraph(f"Block: {block_selected}", styles["Normal"]))

    elements.append(Spacer(1,20))

    elements.append(Paragraph(f"CEF Total Score: {cef_total}/36", styles["Heading2"]))

    elements.append(Spacer(1,20))

    cef_table_data = []

    for label, score in zip(GROUP_LABELS, group_totals):

        cef_table_data.append([label, score])

    cef_table = Table(cef_table_data)

    elements.append(cef_table)

    elements.append(Spacer(1,20))

    elements.append(Paragraph(f"Safeguarding Score: {safeguarding_total}/5", styles["Heading2"]))

    elements.append(Spacer(1,20))

    safe_data = []

    for q in SAFEGUARDING_QUESTIONS:

        score = person_data[q]

        safe_data.append([q, score])

    safe_table = Table(safe_data)

    elements.append(safe_table)

    doc.build(elements)

    buffer.seek(0)

    return buffer

pdf = generate_pdf()

st.download_button(
    label="Download PDF Report",
    data=pdf,
    file_name=f"{coach}_CEF_Report.pdf",
    mime="application/pdf"
)
