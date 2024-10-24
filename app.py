
import warnings
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import requests
warnings.filterwarnings('ignore')


def get_news():
    url = "https://google-news13.p.rapidapi.com/search"
    
    querystring = {"keyword":"Indian Power Sector News","lr":"en-US"}
    
    headers = {
    	"x-rapidapi-key": "9fe8241a5amsh50ee664f06df7d9p19dae4jsne3ec44b9ef5e",
    	"x-rapidapi-host": "google-news13.p.rapidapi.com"
    }
    
    response = requests.get(url, headers=headers, params=querystring)
    
    response = response.json()

    response = response['items']
    st.divider()
    st.markdown('''News!!!''')
    st.divider()
    for i in range(5):
        st.markdown(f"{i+1}.{response[i]['title']}")
        st.write(f"    {response[i]['snippet']}")
# Sample Data
growth_predictions1 = requests.get("https://stockapi-production-7c29.up.railway.app/growth_predictions")
growth_predictions = {
    '1 Day': [],
    '1 Week': [],
    '1 Month': [],
}
a = growth_predictions1.json()

for i in a['1 Day']:
    for j in i:
        growth_predictions['1 Day'].append(i[j])
for i in a['1 Week']:
    for j in i:
        growth_predictions['1 Week'].append(i[j])
for i in a['1 Month']:
    for j in i:
        growth_predictions['1 Month'].append(i[j])

companies = ['ADANIGREEN.NS', 'ADANIPOWER.NS', 'NTPC.NS',
             'POWERGRID.NS', 'RPOWER.NS', 'TATAPOWER.NS', 'JSWENERGY.NS']

# Streamlit app configuration
st.set_page_config(page_title="Power Sector Stock Predictions", layout="wide")

# Extracting the role from the URL parameters using st.query_params
query_params = st.experimental_get_query_params()
role = query_params.get("role", ["Investor"])[0]  # Default to 'Investor' if no role is provided
hide_streamlit_style = """
    <style>
    .stAlert {display: none;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
# Custom inline CSS for styling
st.markdown("""
    <style>
    body {
        background-color: #f4f7fa;
        font-family: 'Roboto', sans-serif;
    }
    .main-title {
        text-align: center;
        color: #022c4f;
        font-size: 2.5em;
        margin-top: -50px;
    }
    .subheader {
        font-size: 1.5em;
        color: #022c4f;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    .plot-container {
        background-color: #ffffff;
        padding: 40px;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
    }
    .btn-custom {
        padding: 10px 20px;
        border-radius: 8px;
        background-color: #28a745;
        color: white;
        text-align: center;
        display: inline-block;
    }
    .btn-custom:hover {
        background-color: #22a03b;
    }
    .plot-container .stButton button {
        background-color: #0056b3;
        color: white;
    }
    .plot-container .stButton button:hover {
        background-color: #004494;
        transform: scale(1.05);
    }
    </style>
    """, unsafe_allow_html=True)

# Function for Investor page
def investor_page():
    st.markdown("<h1 class='main-title'>Investor Dashboard</h1>", unsafe_allow_html=True)

    avg_growth_1_day = np.mean(growth_predictions['1 Day'])
    avg_growth_1_week = np.mean(growth_predictions['1 Week'])
    avg_growth_1_month = np.mean(growth_predictions['1 Month'])

    fig = go.Figure(go.Bar(
        x=['1 Day', '1 Week', '1 Month'],
        y=[avg_growth_1_day, avg_growth_1_week, avg_growth_1_month],
        marker_color='#0683a9'
    ))

    fig.update_layout(title="Investor Sector-Wide Average Growth Predictions",
                      xaxis_title="Time Period", yaxis_title="Growth (%)", template="plotly_white")

    st.plotly_chart(fig)

    st.markdown("""
        *Description:*
        - This graph displays the average growth predictions for the entire power sector.
        - It shows the expected percentage growth over different time periods such as 1 day, 1 week, and 1 month.
        - As an investor, this information helps you evaluate sector-wide trends and opportunities for potential investment.
    """)
    get_news()

# Function for Business Owner page
def business_owner_page():
    st.markdown("<h1 class='main-title'>Business Owner Dashboard</h1>", unsafe_allow_html=True)

    fig = go.Figure()

    fig.add_trace(go.Bar(x=companies, y=growth_predictions['1 Day'], name="Growth for 1 Day", marker_color='#0056b3'))
    fig.add_trace(go.Bar(x=companies, y=growth_predictions['1 Week'], name="Growth for 1 Week", marker_color='#06beec'))
    fig.add_trace(
        go.Bar(x=companies, y=growth_predictions['1 Month'], name="Growth for 1 Month", marker_color='#022c4f'))

    fig.update_layout(title="Business Owner Company-Wise Growth Predictions",
                      xaxis_title="Company", yaxis_title="Growth (%)", barmode='group', template="plotly_white")

    st.plotly_chart(fig)

    st.markdown("""
        *Description:*
        - This graph illustrates company-wise growth predictions for the power sector.
        - Business owners can use this data to analyze competitors' performance and make strategic decisions to grow their own business.
    """)
    get_news()

# Function for Policymaker page with two separated plots
def policymaker_page():
    st.markdown("<h1 class='main-title'>Policymaker Dashboard</h1>", unsafe_allow_html=True)

    st.markdown("<div class='subheader'>Company-Wise Growth Predictions</div>", unsafe_allow_html=True)

    fig1 = go.Figure()

    fig1.add_trace(go.Bar(x=companies, y=growth_predictions['1 Day'], name="Growth for 1 Day", marker_color='#0056b3'))
    fig1.add_trace(
        go.Bar(x=companies, y=growth_predictions['1 Week'], name="Growth for 1 Week", marker_color='#06beec'))
    fig1.add_trace(
        go.Bar(x=companies, y=growth_predictions['1 Month'], name="Growth for 1 Month", marker_color='#022c4f'))

    fig1.update_layout(xaxis_title="Company", yaxis_title="Growth (%)", barmode='group', template="plotly_white")

    st.plotly_chart(fig1)

    st.markdown("""
        *Description:*
        - This graph shows company-specific growth predictions over various time periods (1 day, 1 week, 1 month).
        - Policymakers can use this data to monitor the performance of individual companies and track their progress in the power sector.
    """)

    st.markdown("<div class='subheader'>Sector-Wide Average Growth Predictions</div>", unsafe_allow_html=True)

    fig2 = go.Figure(go.Bar(
        x=['1 Day', '1 Week', '1 Month'],
        y=[np.mean(growth_predictions['1 Day']), np.mean(growth_predictions['1 Week']),
           np.mean(growth_predictions['1 Month'])],
        marker_color='#0683a9'
    ))

    fig2.update_layout(xaxis_title="Time Period", yaxis_title="Growth (%)", template="plotly_white")

    st.plotly_chart(fig2)

    st.markdown("""
        *Description:*
        - This graph represents the sector-wide average growth predictions over different time periods.
        - Policymakers can use this information to assess the overall health and progress of the power sector and make informed decisions regarding policy and regulation.
    """)
    get_news()

# Display the corresponding page based on the role in the URL
if role == "Investor":
    investor_page()
elif role == "Business Owner":
    business_owner_page()
else:
    policymaker_page()
