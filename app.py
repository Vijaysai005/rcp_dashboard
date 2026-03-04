import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import io

# --- 1. MOCK CPG DATA (CSV I/O) ---
# This simulates the backend database for all 4 modules
csv_raw = """Module,Category,Label,Value,Trend,Status,Retailer,SKU,Description,SAP_ID,Subtext
DataMgmt,Quality,Nielsen POS,98,,Excellent,,,,98% Verified
DataMgmt,Quality,Internal Shipments,100,,Excellent,,,,Synced
DataMgmt,Quality,Trade Planner,85,,Good,,,,Action Req
DataMgmt,Quality,IRI Data,92,,Good,,,,Verified
DataMgmt,Mapping,,,Walmart,WMT-RF-200,Reynolds Wrap 200sqft,1000234567,Mapped,
DataMgmt,Mapping,,,Target,TGT-RF-075,Reynolds Wrap 75sqft,1000234568,Mapped,
DataMgmt,Mapping,,,Kroger,KRO-HB-13G,Hefty Strong 13G Trash,2000456789,Unmapped,
BI,KPI,Market Share,23.4%,+1.2%,Positive,,,,Target: 22.5%
BI,KPI,Velocity,4.2,-0.3,Negative,,,,Target: 4.5
BI,KPI,Gross Margin,34.8%,+2.1%,Positive,,,,Target: 33.0%
BI,KPI,Trade ROI,2.8x,+0.4x,Positive,,,,Target: 2.5x
"""

@st.cache_data
def get_cpg_data():
    return pd.read_csv(io.StringIO(csv_raw))

df = get_cpg_data()

# --- 2. GLOBAL UI STYLING ---
st.set_page_config(layout="wide", page_title="Reynolds Analytics Toolkit")

st.markdown("""
<style>
    /* Dark Mode Sidebar */
    [data-testid="stSidebar"] { background-color: #0F172A; border-right: 1px solid #1E293B; }
    
    /* Sidebar Buttons - Left Aligned with Eye Icon Style */
    .stButton > button {
        width: 100%; border: none; background-color: transparent; color: #94A3B8;
        text-align: left; padding: 12px 15px; font-size: 15px; transition: 0.3s;
        display: flex; align-items: center; justify-content: flex-start;
    }
    .stButton > button:hover { background-color: #1E293B; color: #38BDF8; }
    
    /* Blue Active State Highlight from Image */
    .nav-active button { 
        background-color: #2563EB !important; 
        color: white !important; 
        border-radius: 8px; 
        font-weight: 600; 
    }

    /* Card & Gauge Containers */
    .card { background: white; padding: 18px; border-radius: 12px; border: 1px solid #E2E8F0; text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
    .status-pill { padding: 3px 12px; border-radius: 20px; font-size: 11px; font-weight: 700; }
    .pill-excellent { color: #10B981; background: #DCFCE7; }
    .pill-good { color: #D97706; background: #FEF3C7; }
    
    /* KPI Styling */
    .trend-pos { color: #10B981; font-weight: bold; }
    .trend-neg { color: #EF4444; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("<h2 style='color:white; margin-bottom:0;'>Reynolds</h2><p style='color:#64748B; font-size:12px;'>CPG Analytics Toolkit</p>", unsafe_allow_html=True)
    st.write("---")
    
    if 'page' not in st.session_state: 
        st.session_state.page = "Data Management"
    
    menu_items = {
        "Data Management": "👁️",
        "Unified BI": "📊",
        "TPO Simulator": "🎯",
        "Gen AI Assistant": "💬"
    }

    for label, icon in menu_items.items():
        is_active = "nav-active" if st.session_state.page == label else ""
        st.markdown(f'<div class="{is_active}">', unsafe_allow_html=True)
        if st.button(f"{icon} {label}", key=f"nav_{label}"):
            st.session_state.page = label
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.sidebar.markdown("<br><br><br><p style='color:#475569; font-size:11px;'>© 2026 Reynolds Consumer Products</p>", unsafe_allow_html=True)

# --- 4. MODULE CONTENT ---

# MODULE 1: DATA MANAGEMENT (The Image View)
if st.session_state.page == "Data Management":
    st.title("Data Governance Portal")
    st.subheader("Data Quality Scorecard")
    
    dq_data = df[(df['Module'] == 'DataMgmt') & (df['Category'] == 'Quality')]
    cols = st.columns(4)
    
    for i, (_, row) in enumerate(dq_data.iterrows()):
        with cols[i]:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.write(f"**{row['Label']}**")
            
            # Gauge Chart (Donut Style)
            color = "#10B981" if row['Value'] >= 95 else "#F59E0B"
            fig = go.Figure(go.Pie(
                values=[row['Value'], 100-row['Value']], 
                hole=.75, 
                marker_colors=[color, "#F1F5F9"], 
                textinfo='none', 
                hoverinfo='none'
            ))
            # SYNTAX FIXED HERE
            fig.update_layout(
                showlegend=False, height=130, margin=dict(t=0,b=0,l=0,r=0),
                annotations=)}%", x=0.5, y=0.5, font_size=20, showarrow=False, font_weight='bold')]
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            
            p_class = "pill-excellent" if row['Status'] == "Excellent" else "pill-good"
            st.markdown(f'<span class="status-pill {p_class}">{row["Status"]}</span>', unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:10px; color:#94A3B8; margin-top:5px;'>{row['Subtext']}</div>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br><h3>SKU Mapping Engine</h3>", unsafe_allow_html=True)
    c1, c2 = st.columns([3, 1])
    search = c1.text_input("🔍 Search by SKU, description, or SAP material...")
    
    map_df = df[df['Module'] == 'DataMgmt'].dropna(subset=['Retailer'])
    map_display = map_df[['Retailer', 'SKU', 'Description', 'SAP_ID', 'Status']]
    
    if search:
        map_display = map_display[map_display['Description'].str.contains(search, case=False)]
        
    st.dataframe(map_display, use_container_width=True, hide_index=True)

# MODULE 2: UNIFIED BI
elif st.session_state.page == "Unified BI":
    st.title("Unified Business Intelligence")
    kpi_data = df[df['Module'] == 'BI']
    cols = st.columns(4)
    
    for i, (_, row) in enumerate(kpi_data.iterrows()):
        with cols[i]:
            t_class = "trend-pos" if row['Status'] == "Positive" else "trend-neg"
            st.markdown(f"""
            <div class="card">
                <div style='color:#64748B; font-size:12px; font-weight:600;'>{row['Label'].upper()}</div>
                <div style='font-size:28px; font-weight:700;'>{row['Value']}</div>
                <div class='{t_class}' style='font-size:14px;'>{row['Trend']} vs Target</div>
                <div style='color:#94A3B8; font-size:11px;'>{row['Subtext']}</div>
            </div>
            """, unsafe_allow_html=True)
            
    st.markdown("<br>", unsafe_allow_html=True)
    st.info("💡 Proactive Insight: Hefty Strong 13G velocity at Walmart is trending 4% above forecast.")

# MODULE 3: TPO SIMULATOR
elif st.session_state.page == "TPO Simulator":
    st.header("Trade Promo Optimizer")
    col_in, col_out = st.columns([1, 2])
    with col_in:
        st.selectbox("Retailer", ["Walmart", "Target", "Kroger"])
        st.selectbox("Product Group", ["Aluminum Foil", "Trash Bags", "Food Storage"])
        st.slider("Discount Depth %", 5, 40, 15)
        st.button("Simulate Scenario", type="primary")
    with col_out:
        st.markdown("### Predicted Impact")
        st.table(pd.DataFrame({
            "Metric": ["Volume Lift", "Net Revenue", "Trade Spend", "ROI"],
            "Baseline": ["1.0x", "$450k", "$45k", "1.2x"],
            "Simulated": ["1.24x", "$512k", "$62k", "1.45x"]
        }))

# MODULE 4: GEN AI ASSISTANT
elif st.session_state.page == "Gen AI Assistant":
    st.header("Gen AI Strategy Assistant")
    st.chat_message("assistant").write("Hello! I've analyzed the latest IRI data. Foil margins at Target are down 2% due to increased trade spend. Would you like to see a simulation to correct this?")
    st.chat_input("Show me top 5 margin draggers at Kroger last month...")

