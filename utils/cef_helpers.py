import streamlit as st
import pandas as pd


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


def calculate_group_totals(person_data, question_cols):
    totals = []

    for i in range(0, len(question_cols), 4):
        cols = question_cols[i:i+4]
        scores = pd.to_numeric(person_data[cols], errors="coerce")
        totals.append(round(scores.sum(), 2))

    return totals


def render_cef_section(person_data, question_cols):
    st.subheader("CEF Breakdown")

    group_totals = calculate_group_totals(person_data, question_cols)
    cef_total = round(sum(group_totals), 2)

    st.markdown(f"### Score: **{cef_total} / 36**")

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


def render_safeguarding_section(person_data):
    st.subheader("Safeguarding")

    safeguarding_total = sum(
        pd.to_numeric(person_data[q], errors="coerce")
        for q in SAFEGUARDING_QUESTIONS
    )

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
