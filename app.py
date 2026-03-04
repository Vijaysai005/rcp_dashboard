import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import io

# --- PAGE CONFIG ---
st.set_page_config(page_title="Reynolds CPG Analytics Toolkit", layout="wide")

# --- EXPANDED MOCK CSV DATA (10 COMBINATIONS) ---
csv_data = """Retailer,Product,Market_Share,Velocity,Gross_Margin,Trade_ROI,DOS,SAP_Material,Status
Walmart,Reynolds Wrap 200sqft,23.4,4.2,34.8,2.8,18,1000234567,Mapped
Walmart,Hefty Ultra Strong 30Gal,18.2,3.9,31.5,2.4,22,1000987654,Mapped
Target,Reynolds Wrap 200sqft,22.1,4.2,34.8,2.8,25,1000234567,Mapped
Target,Hefty Ultra Strong 30Gal,19.5,4.5,33.0,2.9,19,1000987654,Mapped
Kroger,Reynolds Wrap 200sqft,21.8,3.8,32.5,2.1,12,1000234567,Unmapped
Kroger,Hefty Ultra Strong 30Gal,17.4,4.1,30.8,2.2,16,1000987654,Mapped
CVS,Reynolds Wrap 200sqft,15.5,2.9,28.5,1.8,8,1000234567,Mapped
CVS,Reynolds Parchment 50sqft,12.1,3.2,27.0,1.5,11,1000112233,Mapped
Walmart,Reynolds Plastic Wrap 100sqft,20.2,4.0,33.5,2.6,20,1000556677,Mapped
Target,Reynolds Bakeware Pan,14.8,3.5,29.2,2.0,14,1000443322,Unmapped
"""
df_master = pd.read_csv(io.StringIO(csv_data))

# --- CUSTOM CSS ---
st.markdown("""
<style>
    .stApp { background-color: #F8F9FA; }
    [data-testid="stSidebar"] { background-color: #0E1629; min-width: 280px !important; }
    
    /* Sidebar Buttons - Left Aligned */
    .stButton > button {
        width: 100%; background-color: transparent; color: #AEB9C8;
        border: none; text-align: left; padding: 12px 20px;
        font-size: 16px; border-radius: 4px; display: flex; align-items: center;
    }
    .stButton > button:hover { background-color: #1E293B; color: #FFFFFF; }
    .stButton > button:focus { background-color: #2563EB !important; color: #FFFFFF !important; }
    
    /* KPI Cards */
    div[data-testid="stMetric"] {
        background-color: white; padding: 15px; border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05); border: 1px solid #E2E8F0;
    }
    
    /* Status Label Alignment */
    .quality-label { text-align: center; font-weight: bold; font-size: 14px; margin-top: -35px; margin-bottom: 20px; }
    .status-excellent { color: #10B981; }
    .status-good { color: #F59E0B; }
</style>
""", unsafe_allow_html=True)

# --- NAVIGATION ---
if 'page' not in st.session_state: st.session_state.page = 'UBI'
def nav(p): st.session_state.page = p

with st.sidebar:
    st.markdown("<h2 style='color:white; margin-bottom:0;'>Reynolds</h2><p style='color:#64748B;'>Analytics Toolkit</p>", unsafe_allow_html=True)
    st.button("📊  Unified Business Intelligence", on_click=nav, args=('UBI',))
    st.button("📈  TPO Simulator", on_click=nav, args=('TPO',))
    st.button("✨  Gen AI Assistant", on_click=nav_to, args=('AI',))
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.button("🗄️  Data Management", on_click=nav, args=('DM',))
    st.sidebar.markdown("---")
    st.sidebar.caption("© 2026 Reynolds Consumer Products")

# --- REFINED DONUT COMPONENT ---
def draw_quality_donut(label, value, color, status_text):
    fig = go.Figure(data=[go.Pie(labels=[label, 'Rem'], values=[value, 100-value], hole=.78, 
                                 marker_colors=[color, '#F1F5F9'], textinfo='none', showlegend=False)])
    fig.add_annotation(text=f"<b>{value}%</b>", x=0.5, y=0.5, showarrow=False, font_size=24, font_color="#1E293B")
    fig.update_layout(
        title={'text': label, 'y': 0.9, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top', 'font': {'size': 16, 'color': '#64748B'}}, 
        height=220, margin=dict(t=60, b=0, l=10, r=10), paper_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    status_class = "status-excellent" if status_text == "Excellent" else "status-good"
    st.markdown(f"<div class='quality-label {status_class}'>{status_text}</div>", unsafe_allow_html=True)

# --- PAGES ---

if st.session_state.page == 'UBI':
    st.title("Unified Business Intelligence")
    f1, f2 = st.columns(2)
    s_ret = f1.selectbox("Retailer", df_master['Retailer'].unique())
    s_prod = f2.selectbox("Product", df_master[df_master['Retailer']==s_ret]['Product'].unique())
    
    row = df_master[(df_master['Retailer'] == s_ret) & (df_master['Product'] == s_prod)].iloc
    
    t1, t2, t3 = st.tabs(["KPI Scorecard", "Shipment to Shelf", "Profitability"])
    with t1:
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Market Share", f"{row['Market_Share']}%", "+1.2%")
        k2.metric("Velocity", row['Velocity'], "-0.3")
        k3.metric("Gross Margin", f"{row['Gross_Margin']}%", "+2.1%")
        k4.metric("Trade ROI", f"{row['Trade_ROI']}x", "+0.4x")
        st.subheader("Volume Trends")
        st.line_chart(np.random.randint(200, 600, size=(12, 2)))

    with t2:
        st.subheader("Out-of-Stock Risk Radar")
        st.table(df_master[df_master['Retailer'] == s_ret][['Product', 'DOS']])

elif st.session_state.page == 'TPO':
    st.title("TPO Simulator")
    f1, f2 = st.columns(2)
    f1.selectbox("Retailer", df_master['Retailer'].unique(), key="t_r")
    f2.selectbox("Product", df_master['Product'].unique(), key="t_p")
    st.info("Simulate promotional scenarios to predict volume lift and ROI.")
    st.slider("Discount (%)", 5, 50, 20)
    st.button("Generate Forecast", type="primary")

elif st.session_state.page == 'DM':
    st.title("Data Management Portal")
    
    # Data Quality Scorecard Section
    st.subheader("Data Quality Scorecard")
    d1, d2, d3, d4 = st.columns(4)
    with d1: draw_quality_donut("Nielsen POS", 98, "#10B981", "Excellent")
    with d2: draw_quality_donut("Internal Shipments", 100, "#3B82F6", "Excellent")
    with d3: draw_quality_donut("Trade Planner", 85, "#F59E0B", "Good")
    with d4: draw_quality_donut("IRI Data", 92, "#8B5CF6", "Good")

    st.markdown("---")
    
    # SKU Mapping Engine Section with Filters (Aligned with Image)
    st.subheader("SKU Mapping Engine")
    
    c_s1, c_s2, c_s3 = st.columns()
    search_q = c_s1.text_input("🔍 Search by SKU, description, or retailer...")
    status_q = c_s2.selectbox("Status", ["All", "Mapped", "Unmapped"])
    material_q = c_s3.selectbox("Retailer", ["All"] + list(df_master['Retailer'].unique()))

    # Apply Filters
    df_map = df_master.copy()
    if status_q != "All": df_map = df_map[df_map['Status'] == status_q]
    if material_q != "All": df_map = df_map[df_map['Retailer'] == material_q]
    if search_q: df_map = df_map[df_map['Product'].str.contains(search_q, case=False) | df_map['Retailer SKU'].str.contains(search_q, case=False)]

    st.dataframe(df_map[['Retailer', 'Product', 'SAP_Material', 'Status']], use_container_width=True, hide_index=True)

elif st.session_state.page == 'AI':
    st.title("Gen AI Assistant")
    st.chat_message("assistant").write("Hello! I can help you identify trends or margin draggers. What would you like to know?")
    st.text_input("Ask about your CPG data...")
