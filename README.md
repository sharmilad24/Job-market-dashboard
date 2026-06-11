# Job Market Analytics Dashboard

An end-to-end data project analyzing 300+ real job postings across 
Data Analyst, Data Engineer, and ML Engineer roles.

## Live Demo
🔗 [Click here to try the dashboard](https://sharmila-job-market.streamlit.app)

## What it does
- Collects 300+ job postings via the Adzuna REST API
- Cleans and structures raw data using Pandas
- Extracts 15+ skill features from job descriptions
- Trains a Random Forest classifier to predict job seniority with 67.8% accuracy
- Displays interactive charts and filters via Streamlit and Plotly

## Key findings
- SQL was the most in-demand skill, appearing in 51 out of 293 postings
- Python ranked second, appearing in 38 postings
- Senior roles averaged $166,819 vs $86,959 for Junior roles — an $80k gap
- Salary was the strongest predictor of seniority (feature importance: 0.87)

## Tech stack
Python · Pandas · Scikit-learn · Streamlit · Plotly · REST API · Git

## How to run locally
git clone https://github.com/sharmilad24/Job-market-dashboard
cd Job-market-dashboard
pip install -r requirements.txt
python collect.py
python clean.py
python model.py
streamlit run app.py

## Project structure
data/          → raw and cleaned CSV files + saved ML model
collect.py     → pulls job postings from Adzuna API
clean.py       → cleans data and engineers skill features
model.py       → trains and evaluates Random Forest classifier
app.py         → Streamlit dashboard
