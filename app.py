import streamlit as st
import pandas as pd
import plotly.express as px
import pickle

st.set_page_config(page_title="Job Market Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("data/clean_jobs.csv")

df = load_data()

# ── SIDEBAR FILTERS ──────────────────────────────────────────
st.sidebar.title("Filters")
seniority = st.sidebar.multiselect(
    "Seniority level",
    options=df["seniority"].unique(),
    default=df["seniority"].unique()
)
df_filtered = df[df["seniority"].isin(seniority)]

# ── HEADER ───────────────────────────────────────────────────
st.title("Job Market Analytics Dashboard")
st.markdown("Analyzing real job postings across Data, Analytics, and ML roles")

# ── METRICS ROW ──────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Jobs", len(df_filtered))
col2.metric("Avg Salary", f"${df_filtered['salary_avg'].mean():,.0f}")
col3.metric("Companies", df_filtered["company"].nunique())
col4.metric("Locations", df_filtered["location"].nunique())

st.divider()

# ── CHARTS ───────────────────────────────────────────────────
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Top skills in demand")
    skill_cols = ["python","sql","tableau","power_bi","spark","aws",
                  "excel","machine_learning","pytorch","tensorflow","pandas","dbt"]
    skill_cols = [c for c in skill_cols if c in df.columns]
    skill_counts = df_filtered[skill_cols].sum().sort_values(ascending=False)
    fig1 = px.bar(
        x=skill_counts.values,
        y=skill_counts.index,
        orientation="h",
        color=skill_counts.values,
        color_continuous_scale="Purples",
        labels={"x": "Jobs mentioning skill", "y": "Skill"}
    )
    st.plotly_chart(fig1, use_container_width=True)

with col_right:
    st.subheader("Salary by seniority")
    fig2 = px.box(
        df_filtered,
        x="seniority",
        y="salary_avg",
        color="seniority",
        color_discrete_sequence=["#9FE1CB","#7F77DD","#EF9F27"],
        labels={"salary_avg": "Salary (USD)", "seniority": "Level"}
    )
    st.plotly_chart(fig2, use_container_width=True)

# ── SKILLS GAP TOOL ──────────────────────────────────────────
st.divider()
st.subheader("Skills gap analyzer")
st.markdown("Select a role to see which skills appear most often in those postings")

role_filter = st.selectbox("Choose a role", df["title"].value_counts().head(20).index)
role_df = df[df["title"] == role_filter]
if len(role_df) > 0:
    role_skills = role_df[skill_cols].sum().sort_values(ascending=False).head(8)
    fig3 = px.bar(
        x=role_skills.index,
        y=role_skills.values,
        color=role_skills.values,
        color_continuous_scale="Teal",
        labels={"x": "Skill", "y": "Frequency"}
    )
    st.plotly_chart(fig3, use_container_width=True)

# ── ML PREDICTOR ─────────────────────────────────────────────
st.divider()
st.subheader("Predict job seniority with ML")
st.markdown("Enter job details and the model predicts Junior / Mid / Senior")

try:
    with open("data/model.pkl", "rb") as f:
        model, le, feature_cols = pickle.load(f)

    input_salary = st.slider("Expected salary ($)", 30000, 200000, 70000, 5000)
    selected_skills = st.multiselect("Skills mentioned", options=skill_cols)

    if st.button("Predict"):
        input_row = {col: 0 for col in feature_cols}
        input_row["salary_avg"] = input_salary
        for s in selected_skills:
            if s in input_row:
                input_row[s] = 1
        X_input = pd.DataFrame([input_row])
        pred = model.predict(X_input)
        label = le.inverse_transform(pred)[0]
        st.success(f"Predicted seniority: **{label}**")
except FileNotFoundError:
    st.warning("Run model.py first to enable predictions")