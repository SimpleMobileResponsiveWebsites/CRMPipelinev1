import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# Initialize session state for the deals DataFrame if it doesn't exist
if 'df' not in st.session_state:
    deals_data = {
        "Stage": [],
        "Deal": [],
        "Company": [],
        "Value": []
    }
    st.session_state.df = pd.DataFrame(deals_data)

# Header
st.title("Pipedrive CRM")

# Top menu
col1, col2, col3, col4 = st.columns([1, 6, 2, 1])
with col1:
    st.button("🔍")
with col2:
    st.text_input("Search Pipedrive")
with col3:
    st.button("+ Deal")
with col4:
    st.button("👤")

# Pipeline stages
stages = ["Qualified", "Contact Made", "Demo Scheduled", "Proposal Made", "Negotiations Started"]

# Function to add a new deal
def add_deal(stage, deal, company, value):
    new_deal = pd.DataFrame({"Stage": [stage], "Deal": [deal], "Company": [company], "Value": [value]})
    st.session_state.df = pd.concat([st.session_state.df, new_deal], ignore_index=True)

# Function to move a deal to a new stage
def move_deal(deal_name, new_stage):
    st.session_state.df.loc[st.session_state.df['Deal'] == deal_name, 'Stage'] = new_stage

# Form to enter a new deal
st.sidebar.subheader("Add a new deal")
with st.sidebar.form("add_deal_form"):
    stage = st.selectbox("Stage", stages)
    deal = st.text_input("Deal Name")
    company = st.text_input("Company Name")
    value = st.number_input("Value", min_value=0, step=1)
    submitted = st.form_submit_button("Add Deal")
    if submitted:
        add_deal(stage, deal, company, value)
        st.sidebar.success("Deal added successfully!")

# Form to move a deal to a new stage
st.sidebar.subheader("Move/Convert a deal")
with st.sidebar.form("move_deal_form"):
    if not st.session_state.df.empty:
        deal_name = st.selectbox("Select Deal", st.session_state.df['Deal'])
        new_stage = st.selectbox("New Stage", stages)
        move_submitted = st.form_submit_button("Move Deal")
        if move_submitted:
            move_deal(deal_name, new_stage)
            st.sidebar.success("Deal moved successfully!")
    else:
        st.sidebar.write("No deals available to move.")

# Display pipeline
st.subheader("Sales pipeline")
cols = st.columns(len(stages))

for i, stage in enumerate(stages):
    with cols[i]:
        st.write(f"**{stage}**")
        stage_deals = st.session_state.df[st.session_state.df["Stage"] == stage]
        st.write(f"€{stage_deals['Value'].sum()} · {len(stage_deals)} deals")
        for _, deal in stage_deals.iterrows():
            with st.expander(f"{deal['Deal']}"):
                st.write(f"{deal['Company']}")
                st.write(f"€{deal['Value']}")

# Footer
st.write("---")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.button("DELETE")
with col2:
    st.button("LOST")
with col3:
    st.button("WON")
with col4:
    st.button("MOVE/CONVERT")

# Sidebar
with st.sidebar:
    st.image("https://placeholder.com/wp-content/uploads/2018/10/placeholder.com-logo1.png", width=50)
    st.button("💰")
    st.button("📋")
    st.button("🔔")
    st.button("📅")
    st.button("📊")
    st.button("📦")
    st.button("🏠")
