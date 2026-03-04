import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import io

# --- PAGE CONFIG ---
st.set_page_config(page_title="Reynolds CPG Analytics Toolkit", layout="wide")

# --- MOCK CSV DATA INGESTION ---
csv_data = """Retailer,Product,Market_Share,Velocity,Gross_Margin,Trade_ROI,DOS,SAP_Material,Status
Walmart,Reynolds Wrap 200sqft,23.4,4.2,34.8,2.8,18,1000234567,Mapped
Walmart,Hefty Ultra Strong 30Gal,18.2,3.9,31.5,2.4,22,1000987654,Mapped
Target,Reynolds Wrap 200sqft,22.1,4.2,34.8,2.8,25,1000234567,Mapped
Target,Hefty Ultra Strong 30Gal,19.5,4.5,33.0,2.9,19,1000987654,Mapped
Kroger,Reynolds Wrap 200sqft,21.8,3.8,32.5,2.1,12,1000234567,Unmapped
Kroger,Hefty Ultra Strong 30Gal,17.4,4.1,30.8,2.2,16,1000987654,Mapped
CVS,Reynolds Wrap 200sqft,15.5,2.9,28.5,1.8,8,1000234567,Mapped
CVS,Hefty Ultra Strong 30Gal,12.1,3.2,27.0,1.5,11,1000987654,Mapped
"""
df_master = pd.read_csv(io.StringIO(csv_data))

# --- CUSTOM CSS ---
st.markdown("""
<style>
    .stApp { background-color: #F8F9FA; }
    [data-testid="stSidebar"] { background-color: #0E1629; min-width: 280px !important; }
    
    /* Sidebar Buttons */
    .stButton > button {
        width: 100%; background-color: transparent; color: #AEB9C8;
        border: none; text-align: left; padding: 12px 20px;
        font-size: 16px; border-radius: 4px; display: flex; align-items: center;
    }
    .stButton > button:hover { background-color: #1E293B; color: #FFFFFF; }
    .stButton > button:focus { background-color: #2563EB !important; color: #FFFFFF !important; }
    
    /* KPI Metric Cards */
    div[data-testid="stMetric"] {
        background-color: white; padding: 15px; border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05); border: 1px solid #E2E8F0;
    }
    
    /* Quality Labels */
    .quality-label {
        text-align: center; font-weight: bold; font-size: 14px; margin-top: -20px;
    }
    .status-excellent { color: #10B981; }
    .status-good { color: #F59E0B; }
</style>
""", unsafe_allow_html=True)

# --- NAVIGATION ---
if 'page' not in st.session_state: st.session_state.page = 'UBI'
def nav(p): st.session_state.page = p

with st.sidebar:
    st.markdown("<h2 style='color:white;'>Reynolds</h2><p style='color:#64748B;'>Analytics Toolkit</p>", unsafe_allow_html=True)
    st.button("📊  Unified Business Intelligence", on_click=nav, args=('UBI',))
    st.button("📈  TPO Simulator", on_click=nav, args=('TPO',))
    st.button("✨  Gen AI Assistant", on_click=nav, args=('AI',))
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.button("🗄️  Data Management", on_click=nav, args=('DM',))
    st.sidebar.markdown("---")
    st.sidebar.caption("© 2026 Reynolds Consumer Products")

# --- DONUT COMPONENT WITH QUALITY LABELS ---
def draw_quality_donut(label, value, color, status_text):
    fig = go.Figure(data=[go.Pie(labels=[label, 'Rem'], values=[value, 100-value], hole=.75, 
                                 marker_colors=[color, '#E2E8F0'], textinfo='none', showlegend=False)])
    fig.add_annotation(text=f"<b>{value}%</b>", x=0.5, y=0.5, showarrow=False, font_size=22)
    fig.update_layout(title={'text': label, 'x': 0.5, 'font': {'size': 16, 'color': '#1E293B'}}, 
                      height=220, margin=dict(t=50, b=10, l=10, r=10), paper_bgcolor="rgba(0,0,0,0)")
    
    st.plotly_chart(fig, use_container_width=True)
    status_class = "status-excellent" if status_text == "Excellent" else "status-good"
    st.markdown(f"<div class='quality-label {status_class}'>{status_text}</div>", unsafe_allow_html=True)

# --- PAGE LOGIC ---

# 1. UNIFIED BUSINESS INTELLIGENCE
if st.session_state.page == 'UBI':
    st.title("Unified Business Intelligence")
    c1, c2 = st.columns(2)
    sel_ret = c1.selectbox("Filter Retailer", df_master['Retailer'].unique())
    sel_prod = c2.selectbox("Filter Product", df_master['Product'].unique())
    
    # Filter Data for KPI
    row = df_master[(df_master['Retailer'] == sel_ret) & (df_master['Product'] == sel_prod)].iloc[0]
    
    t1, t2, t3 = st.tabs(["Enterprise KPI Scorecard", "Shipment to Shelf", "SKU & Customer Profitability"])
    with t1:
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Market Share", f"{row['Market_Share']}%", "+1.2%")
        m2.metric("Velocity", row['Velocity'], "-0.3")
        m3.metric("Gross Margin", f"{row['Gross_Margin']}%", "+2.1%")
        m4.metric("Trade ROI", f"{row['Trade_ROI']}x", "+0.4x")
        st.subheader("Market Share Tracker (12 Month)")
        st.line_chart(pd.DataFrame(np.random.randn(12, 3), columns=['Reynolds', 'Competitor', 'Private Label']))

    with t2:
        st.subheader("Inventory Health Matrix")
        st.table(df_master[df_master['Retailer'] == sel_ret][['Product', 'DOS']])
        if row['DOS'] < 10: st.error(f"⚠️ Critical OOS Risk for {sel_prod}")

    with t3:
        st.subheader("Margin Waterfall")
        st.plotly_chart(go.Figure(go.Waterfall(x=["Gross", "COGS", "Trade", "Net"], y=[100, -40, -15, 45])), use_container_width=True)

# 2. TPO SIMULATOR
elif st.session_state.page == 'TPO':
    st.title("TPO Simulator")
    f1, f2 = st.columns(2)
    s_ret = f1.selectbox("Retailer", df_master['Retailer'].unique(), key="tpo_r")
    s_prod = f2.selectbox("Product", df_master['Product'].unique(), key="tpo_p")
    
    l, r = st.columns([1, 2])
    with l:
        st.info("Promo Parameters")
        st.slider("Discount Amount (%)", 5, 50, 20)
        st.button("Run Simulation", type="primary", use_container_width=True)
    with r:
        st.subheader("Scenario Comparison")
        st.table(pd.DataFrame({"Metric": ["Volume", "Revenue", "ROI"], "Baseline": ["42,000", "$168k", "0.0x"], "Scenario 1": ["56,700", "$208k", "1.6x"]}))

# 3. GEN AI ASSISTANT
elif st.session_state.page == 'AI':
    st.title("Gen AI NL Assistant")
    st.chat_message("assistant").write("Hello! I can help you analyze Reynolds products and trade effectiveness. What's your question?")
    st.text_input("Ask a question about your CPG data...")
    st.warning("**Insight Feed**: Aluminum costs rose 3%, impacting foil margins. Expected impact: -$1.2M")

# 4. DATA MANAGEMENT (Bottom of sidebar)
elif st.session_state.page == 'DM':
    st.title("Data Management Portal")
    f1, f2 = st.columns(2)
    f1.selectbox("Data Source", ["All Sources", "Nielsen", "IRI", "SAP"], key="dm_r")
    f2.selectbox("Product Line", ["All", "Aluminum Foil", "Trash Bags"], key="dm_c")

    st.subheader("Data Quality Scorecard")
    d1, d2, d3, d4 = st.columns(4)
    with d1: draw_quality_donut("Nielsen POS", 98, "#10B981", "Excellent")
    with d2: draw_quality_donut("Internal Shipments", 100, "#3B82F6", "Excellent")
    with d3: draw_quality_donut("Trade Planner", 85, "#F59E0B", "Good")
    with d4: draw_quality_donut("IRI Data", 92, "#8B5CF6", "Good")

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.subheader("SKU Mapping Engine")
    st.dataframe(df_master[['Retailer', 'Product', 'SAP_Material', 'Status']], use_container_width=True, hide_index=True)
