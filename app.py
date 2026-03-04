import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# --- PAGE CONFIG ---
st.set_page_config(page_title="Reynolds CPG Analytics Toolkit", layout="wide")

# --- CUSTOM CSS FOR ENTERPRISE UI ---
st.markdown("""
<style>
    /* Main Background */
    .stApp { background-color: #F8F9FA; }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #0E1629;
        color: white;
        min-width: 260px !important;
    }
    
    /* Left-aligned Sidebar Buttons */
    div.stButton > button {
        width: 100%;
        background-color: transparent;
        color: #AEB9C8;
        border: none;
        text-align: left;
        padding: 10px 20px;
        font-size: 16px;
        border-radius: 0px;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #1E293B;
        color: #FFFFFF;
    }
    div.stButton > button:focus {
        background-color: #2563EB;
        color: #FFFFFF;
        border-left: 4px solid #FFFFFF;
    }

    /* KPI Cards */
    .kpi-card {
        background-color: white;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    /* Tab Navigation Styling */
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: transparent;
        border: none;
        color: #64748B;
    }
    .stTabs [aria-selected="true"] {
        color: #2563EB !important;
        border-bottom: 2px solid #2563EB !important;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.image("https://upload.wikimedia.org", width=150) # Placeholder for Reynolds Logo
    st.markdown("### CPG Analytics Toolkit")
    st.markdown("---")
    
    # Navigation Buttons (Left Aligned)
    btn_dm = st.button("🗄️ Data Management")
    btn_bi = st.button("📊 Unified Business Intelligence")
    btn_tpo = st.button("📈 TPO Simulator")
    btn_ai = st.button("✨ Gen AI Assistant")
    
    st.sidebar.markdown("---")
    st.sidebar.caption("© 2026 Reynolds Consumer Products")

# --- MAIN CONTENT AREA ---

# Module 1: Data Management (Default View)
st.title("Data Management Portal")
    
col1, col2 = st.columns([2, 1])
with col1:
    st.subheader("SKU Mapping Engine")
    mapping_data = pd.DataFrame({
        "Retailer": ["Walmart", "Target", "Kroger", "CVS"],
        "Retailer SKU": ["WMT-RF-200-01", "TGT-TB-30-50", "KRG-PW-100", "CVS-AF-75"],
        "Product Description": ["Reynolds Wrap Aluminum Foil 200sqft", "Hefty Ultra Strong 30Gal", "Reynolds Plastic Wrap 100sqft", "Reynolds Foil 75sqft"],
        "SAP Material #": ["1000234567", "1000987654", "1000556677", "1000334455"],
        "Status": ["Mapped", "Mapped", "Unmapped", "Mapped"]
    })
    st.dataframe(mapping_data, use_container_width=True)

with col2:
    st.subheader("Data Quality Scorecard")
    # Gauges or Metrics for Data Freshness
    st.metric("Nielsen POS", "98%", "Excellent")
    st.metric("Internal Shipments", "100%", "Excellent")
    st.metric("Trade Planner", "85%", "-2%", delta_color="normal")
    st.metric("IRI Data", "92%", "Good")

st.markdown("---")

# Module 2: Unified Business Intelligence (Mockup Structure)
st.title("Unified Business Intelligence")
tab1, tab2, tab3 = st.tabs(["Enterprise KPI Scorecard", "Shipment to Shelf", "SKU & Customer Profitability"])

with tab1:
    # KPI Cards
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Market Share", "23.4%", "+1.2%", help="Target: 22.5%")
    k2.metric("Velocity", "4.2", "-0.3", help="Target: 4.5")
    k3.metric("Gross Margin", "34.8%", "+2.1%", help="Target: 33.0%")
    k4.metric("Trade ROI", "2.8x", "+0.4x", help="Target: 2.5x")
    
    st.subheader("Market Share Tracker (12 Month)")
    chart_data = pd.DataFrame(np.random.randn(12, 3), columns=['Reynolds', 'Competitor A', 'Private Label'])
    st.line_chart(chart_data)

with tab2:
    st.subheader("Inventory Health Matrix (Days of Supply)")
    inventory_data = pd.DataFrame({
        "Retailer": ["Walmart", "Target", "Kroger", "CVS"],
        "Aluminum Foil": [18, 25, 12, 8],
        "Trash Bags": [22, 19, 16, 11],
        "Plastic Wrap": [15, 21, 14, 9]
    })
    st.table(inventory_data.style.background_gradient(cmap='RdYlGn', subset=["Aluminum Foil", "Trash Bags", "Plastic Wrap"]))
    
    st.subheader("OOS Risk Radar")
    st.warning("⚠️ Critical: Reynolds Wrap 200sqft at Kroger (8 Days Supply - High Velocity)")

with tab3:
    st.subheader("Margin Waterfall")
    waterfall_fig = go.Figure(go.Waterfall(
        name = "20", orientation = "v",
        measure = ["relative", "relative", "relative", "total"],
        x = ["Gross Revenue", "COGS", "Trade Spend", "Net Margin"],
        textposition = "outside",
        y = [100, -40, -15, 45],
        connector = {"line":{"color":"rgb(63, 63, 63)"}},
    ))
    st.plotly_chart(waterfall_fig, use_container_width=True)

st.markdown("---")

# Module 3: TPO Simulator
st.title("TPO Simulator")
sim_col1, sim_col2 = st.columns([1, 2])

with sim_col1:
    st.subheader("Promo Parameters")
    st.selectbox("Retailer", ["Walmart", "Target", "Kroger"])
    st.selectbox("Product", ["Reynolds Wrap 200sqft", "Hefty Ultra Strong 30Gal"])
    st.selectbox("Discount Type", ["% Off", "TPR", "Display"])
    st.slider("Discount Amount (%)", 0, 50, 20)
    st.button("Run Simulation", type="primary")

with sim_col2:
    st.subheader("Scenario Comparison")
    # Using dummy columns for visualization
    compare_data = pd.DataFrame({
        "Metric": ["Volume Lift", "Revenue ($)", "Net Margin ($)", "ROI"],
        "Baseline": ["42,000", "$168k", "$58k", "0.0x"],
        "Scenario 1 (Moderate)": ["56,700 (+35%)", "$208k", "$45k", "1.6x"],
        "Scenario 2 (Aggressive)": ["65,100 (+55%)", "$229k", "$38k", "0.9x"]
    })
    st.table(compare_data)
    st.success("💡 Recommendation: Scenario 1 (Moderate) offers the best balance of volume lift and ROI.")

st.markdown("---")

# Module 4: Gen AI Assistant
st.title("Gen AI NL Assistant")
ai_col1, ai_col2 = st.columns([2, 1])

with ai_col1:
    st.chat_message("assistant").write("Hello! I'm your CPG Analytics Assistant. How can I help you today?")
    st.text_input("Ask a question about your CPG data...", placeholder="e.g., Show me top margin draggers at Walmart")
    
with ai_col2:
    st.subheader("Automated Insights")
    st.info("🚨 **Commodity Cost Alert**: Aluminum costs rose 3%, impacting foil margins. Expected Q2 impact: -$1.2M")
    st.info("📈 **Market Share**: Reynolds Wrap gained 1.5 pts in 'Cooking & Baking' category at Target last month.")

# PROACTIVE FOLLOW-UP
# Would you like me to connect this UI to a **live database** or refine the **data visualization** for a specific retailer?
