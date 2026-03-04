import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --- PAGE CONFIG ---
st.set_page_config(page_title="Reynolds CPG Analytics Toolkit", layout="wide")

# --- CUSTOM CSS FOR HIGH-FIDELITY UI ---
st.markdown("""
<style>
    /* Main Background */
    .stApp { background-color: #F8F9FA; }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #0E1629;
        min-width: 280px !important;
    }
    
    /* Left-aligned Sidebar Buttons */
    .stButton > button {
        width: 100%;
        background-color: transparent;
        color: #AEB9C8;
        border: none;
        text-align: left;
        padding: 12px 20px;
        font-size: 16px;
        border-radius: 4px;
        display: flex;
        align-items: center;
        transition: 0.2s;
    }
    .stButton > button:hover {
        background-color: #1E293B;
        color: #FFFFFF;
        border: none;
    }
    /* Active State Mockup */
    .stButton > button:focus {
        background-color: #2563EB !important;
        color: #FFFFFF !important;
        box-shadow: none;
    }

    /* Metric Card Styling */
    div[data-testid="stMetric"] {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border: 1px solid #E2E8F0;
    }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE NAVIGATION ---
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Data Management'

def nav_to(page):
    st.session_state.current_page = page

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color:white; margin-bottom:0;'>Reynolds</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748B; margin-top:0;'>CPG Analytics Toolkit</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Clickable Sidebar Buttons
    st.button("🗄️  Data Management", on_click=nav_to, args=('Data Management',))
    st.button("📊  Unified Business Intelligence", on_click=nav_to, args=('UBI',))
    st.button("📈  TPO Simulator", on_click=nav_to, args=('TPO',))
    st.button("✨  Gen AI Assistant", on_click=nav_to, args=('AI',))
    
    st.sidebar.markdown("---")
    # Global Filters (Affecting all modules)
    st.sidebar.subheader("Global Filters")
    sel_retailer = st.sidebar.selectbox("Select Retailer", ["All Retailers", "Walmart", "Target", "Kroger", "CVS"])
    sel_category = st.sidebar.selectbox("Product Category", ["All", "Aluminum Foil", "Trash Bags", "Plastic Wrap", "Cookware"])
    
    st.sidebar.caption("© 2026 Reynolds Consumer Products")

# --- GAUGE COMPONENT ---
def draw_gauge(label, value, color="#2563EB"):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = value,
        title = {'text': label, 'font': {'size': 16}},
        gauge = {
            'axis': {'range': [0, 100]},
            'bar': {'color': color},
            'bgcolor': "white",
            'steps': [{'range': [0, 85], 'color': '#FEE2E2'}, {'range': [85, 95], 'color': '#FEF3C7'}, {'range': [95, 100], 'color': '#DCFCE7'}]
        }
    ))
    fig.update_layout(height=180, margin=dict(l=20, r=20, t=30, b=20), paper_bgcolor="rgba(0,0,0,0)")
    return fig

# --- MODULE CONTENT ---

# 1. DATA MANAGEMENT PORTAL
if st.session_state.current_page == 'Data Management':
    st.title("Data Management Portal")
    
    st.subheader("Data Quality Scorecard")
    g1, g2, g3, g4 = st.columns(4)
    g1.plotly_chart(draw_gauge("Nielsen POS", 98, "#10B981"), use_container_width=True)
    g2.plotly_chart(draw_gauge("Internal Shipments", 100, "#10B981"), use_container_width=True)
    g3.plotly_chart(draw_gauge("Trade Planner", 85, "#F59E0B"), use_container_width=True)
    g4.plotly_chart(draw_gauge("IRI Data", 92, "#10B981"), use_container_width=True)

    st.markdown("---")
    st.subheader("SKU Mapping Engine")
    col_s1, col_s2, col_s3 = st.columns([2, 1, 1])
    search_sku = col_s1.text_input("Search by SKU or Description", placeholder="e.g. Reynolds Wrap")
    status_filter = col_s2.selectbox("Status", ["All", "Mapped", "Unmapped"])
    sap_filter = col_s3.text_input("SAP Material #")
    
    mapping_data = pd.DataFrame({
        "Retailer": ["Walmart", "Target", "Kroger", "CVS", "Walmart"],
        "Retailer SKU": ["WMT-RF-200-01", "TGT-TB-30-50", "KRG-PW-100", "CVS-AF-75", "WMT-P-50"],
        "Product Description": ["Reynolds Wrap Aluminum Foil 200sqft", "Hefty Ultra Strong 30Gal", "Reynolds Plastic Wrap 100sqft", "Reynolds Foil 75sqft", "Reynolds Parchment 50sqft"],
        "SAP Material #": ["1000234567", "1000987654", "1000556677", "1000334455", "1000112233"],
        "Status": ["Mapped", "Mapped", "Unmapped", "Mapped", "Mapped"]
    })
    st.dataframe(mapping_data, use_container_width=True, hide_index=True)

# 2. UNIFIED BUSINESS INTELLIGENCE
elif st.session_state.current_page == 'UBI':
    st.title("Unified Business Intelligence")
    ubi_tabs = st.tabs(["Enterprise KPI Scorecard", "Shipment to Shelf", "SKU & Customer Profitability"])
    
    with ubi_tabs[0]:
        st.subheader(f"Key Performance Indicators: {sel_retailer}")
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Market Share", "23.4%", "1.2%", help="Target: 22.5%")
        k2.metric("Velocity", "4.2", "-0.3", help="Target: 4.5")
        k3.metric("Gross Margin", "34.8%", "2.1%", help="Target: 33.0%")
        k4.metric("Trade ROI", "2.8x", "0.4x", help="Target: 2.5x")
        
        st.subheader("Market Share Tracker (12 Month)")
        chart_data = pd.DataFrame(np.random.randn(12, 3), columns=['Reynolds', 'Competitor A', 'Private Label'])
        st.line_chart(chart_data)

    with ubi_tabs[1]:
        st.subheader("Inventory Health Matrix (Days of Supply)")
        dos_df = pd.DataFrame({
            "Retailer": ["Walmart", "Target", "Kroger", "CVS"],
            "Aluminum Foil": [18, 25, 12, 8],
            "Trash Bags": [22, 19, 16, 11],
            "Plastic Wrap": [15, 21, 14, 9]
        })
        st.table(dos_df.style.background_gradient(cmap='RdYlGn', subset=["Aluminum Foil", "Trash Bags", "Plastic Wrap"]))
        st.error("🚨 **Critical Risk**: Reynolds Wrap 200sqft at CVS (8 Days Supply) - Critical Risk Level")

    with ubi_tabs[2]:
        st.subheader("Margin Waterfall: Revenue to Net Margin")
        # Waterfall Placeholder
        fig_wf = go.Figure(go.Waterfall(
            orientation = "v",
            measure = ["relative", "relative", "relative", "total"],
            x = ["Gross Revenue", "COGS", "Trade Spend", "Net Margin"],
            y = [100, -42, -18, 40],
            connector = {"line":{"color":"#cbd5e1"}}
        ))
        st.plotly_chart(fig_wf, use_container_width=True)

# 3. TPO SIMULATOR
elif st.session_state.current_page == 'TPO':
    st.title("TPO Simulator")
    sim_col1, sim_col2 = st.columns([1, 2])
    
    with sim_col1:
        st.info("Promo Parameters")
        st.selectbox("Select Target Retailer", ["Walmart", "Target", "Kroger"])
        st.selectbox("Select Product", ["Reynolds Wrap 200sqft", "Hefty Ultra Strong 30Gal"])
        st.selectbox("Discount Type", ["% Off", "TPR", "Display"])
        st.slider("Discount Amount (%)", 0, 50, 20)
        st.slider("Duration (Weeks)", 1, 4, 2)
        st.button("Run Simulation", type="primary", use_container_width=True)

    with sim_col2:
        st.subheader("Scenario Comparison")
        comparison = pd.DataFrame({
            "Metric": ["Predicted Volume", "Predicted Revenue", "Promo Spend", "Predicted ROI"],
            "Baseline": ["42,000", "$168,000", "$0", "0.0x"],
            "Scenario 1 (Moderate)": ["56,700 (+35%)", "$208,656", "$28,000", "1.6x"],
            "Scenario 2 (Aggressive)": ["65,100 (+55%)", "$229,152", "$42,000", "0.9x"]
        })
        st.table(comparison)
        st.success("💡 **Recommendation**: Scenario 1 (Moderate) offers the best balance of volume lift and ROI at 1.6x.")

# 4. GEN AI ASSISTANT
elif st.session_state.current_page == 'AI':
    st.title("Gen AI NL Assistant")
    chat_col, alert_col = st.columns([2, 1])
    
    with chat_col:
        st.chat_message("assistant").write("Hello! I'm your CPG Assistant. I can help analyze Reynolds products and trade effectiveness. What would you like to know?")
        st.text_input("Ask a question about your CPG data...", placeholder="e.g., Show me top margin draggers at Walmart last month")
        st.caption("Try: 'Market share trends' or 'Best promo ROI'")

    with alert_col:
        st.markdown("### Automated Insights")
        st.warning("**Commodity Cost Alert**\nAluminum costs rose 3%, impacting foil margins. Expected Q2 impact: -$1.2M")
        st.info("**Trend Alert**\nMarket share for Reynolds Wrap increased 1.2% at Walmart following Scenario 1 execution.")

