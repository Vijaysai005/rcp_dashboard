import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import io

# --- 1. INTEGRATED CSV DATA (I/O) ---
csv_raw = """Module,Category,Label,Value,Trend,Status,Retailer,SKU,Description,SAP_ID,Subtext
DataMgmt,Quality,Nielsen POS,98,,Excellent,,,,98% Verified
DataMgmt,Quality,Internal Shipments,100,,Excellent,,,,Synced
DataMgmt,Quality,Trade Planner,85,,Good,,,,Action Req
DataMgmt,Quality,IRI Data,92,,Good,,,,Verified
DataMgmt,Mapping,,,Walmart,WMT-RF-200,Reynolds Wrap 200sqft,1000234567,Mapped
DataMgmt,Mapping,,,Target,TGT-RF-075,Reynolds Wrap 75sqft,1000234568,Mapped
DataMgmt,Mapping,,,Kroger,KRO-HB-13G,Hefty Strong 13G Trash,2000456789,Unmapped
BI,KPI,Market Share,23.4%,+1.2%,Positive,,,,Target: 22.5%
BI,KPI,Velocity,4.2,-0.3,Negative,,,,Target: 4.5
BI,KPI,Gross Margin,34.8%,+2.1%,Positive,,,,Target: 33.0%
BI,KPI,Trade ROI,2.8x,+0.4x,Positive,,,,Target: 2.5x
"""

@st.cache_data
def load_data():
    return pd.read_csv(io.StringIO(csv_raw))

df = load_data()

# --- 2. GLOBAL UI STYLING ---
st.set_page_config(layout="wide", page_title="Reynolds Analytics Toolkit")

st.markdown("""
<style>
    /* Dark Mode Sidebar */
    [data-testid="stSidebar"] { 
        background-color: #0F172A; 
        border-right: 1px solid #1E293B; 
    }
    
    /* Left Aligned Eye-Icon Buttons */
    .stButton > button {
        width: 100%; border: none; background-color: transparent; color: #94A3B8;
        text-align: left; padding: 12px 15px; font-size: 15px; transition: 0.3s;
        display: flex; align-items: center; justify-content: flex-start;
    }
    .stButton > button:hover { background-color: #1E293B; color: #38BDF8; }
    
    /* Blue Active State Highlight */
    .active-nav button { 
        background-color: #2563EB !important; 
        color: white !important; 
        border-radius: 8px; 
        font-weight: 600; 
    }

    /* Card & Gauge Containers */
    .card { 
        background: white; padding: 20px; border-radius: 12px; 
        border: 1px solid #E2E8F0; text-align: center; 
        box-shadow: 0 1px 3px rgba(0,0,0,0.05); 
    }
    .status-pill { padding: 3px 12px; border-radius: 20px; font-size: 11px; font-weight: 700; }
    .pill-excellent { color: #10B981; background: #DCFCE7; }
    .pill-good { color: #D97706; background: #FEF3C7; }
</style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("<h2 style='color:white; margin-bottom:0;'>Reynolds</h2><p style='color:#64748B; font-size:12px;'>CPG Analytics Toolkit</p>", unsafe_allow_html=True)
    st.write("---")
    
    if 'current_page' not in st.session_state: 
        st.session_state.current_page = "Data Management"
    
    menu = {
        "Data Management": "👁️", 
        "Unified BI": "📊", 
        "TPO Simulator": "🎯", 
        "Gen AI Assistant": "💬"
    }

    for label, icon in menu.items():
        # Apply blue highlight if active
        is_active = "active-nav" if st.session_state.current_page == label else ""
        st.markdown(f'<div class="{is_active}">', unsafe_allow_html=True)
        if st.button(f"{icon} {label}", key=f"nav_{label}"):
            st.session_state.current_page = label
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- 4. MODULE CONTENT ---

# MODULE 1: DATA MANAGEMENT (Gauges without center text)
if st.session_state.current_page == "Data Management":
    st.header("Data Governance Portal")
    st.subheader("Data Quality Scorecard")
    
    dq_rows = df[(df['Module'] == 'DataMgmt') & (df['Category'] == 'Quality')]
    cols = st.columns(4)
    
    for i, (_, row) in enumerate(dq_rows.iterrows()):
        with cols[i]:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.write(f"**{row['Label']}**")
            
            # Clean Donut Chart (Annotations Removed)
            color = "#10B981" if row['Value'] >= 95 else "#F59E0B"
            fig = go.Figure(go.Pie(
                values=[row['Value'], 100-row['Value']], 
                hole=.75, 
                marker_colors=[color, "#F1F5F9"], 
                textinfo='none', 
                hoverinfo='none'
            ))
            
            fig.update_layout(
                showlegend=False, 
                height=130, 
                margin=dict(t=10, b=10, l=10, r=10)
                # Annotation block removed for cleaner UI
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            
            p_class = "pill-excellent" if row['Status'] == "Excellent" else "pill-good"
            st.markdown(f'<span class="status-pill {p_class}">{row["Status"]}</span>', unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:12px; font-weight:bold; margin-top:5px;'>{row['Value']}%</div>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>### SKU Mapping Engine", unsafe_allow_html=True)
    map_df = df[df['Module'] == 'DataMgmt'].dropna(subset=['Retailer'])
    st.dataframe(map_df[['Retailer', 'SKU', 'Description', 'SAP_ID', 'Status']], use_container_width=True, hide_index=True)

# MODULE 2: UNIFIED BI
elif st.session_state.current_page == "Unified BI":
    st.header("Unified Business Intelligence")
    kpi_rows = df[df['Module'] == 'BI']
    cols = st.columns(4)
    for i, (_, row) in enumerate(kpi_rows.iterrows()):
        with cols[i]:
            t_color = "#10B981" if row['Status'] == "Positive" else "#EF4444"
            st.markdown(f"""
            <div class="card">
                <div style='color:#64748B; font-size:11px; font-weight:700;'>{row['Label'].upper()}</div>
                <div style='font-size:26px; font-weight:700;'>{row['Value']}</div>
                <div style='color:{t_color}; font-size:13px; font-weight:bold;'>{row['Trend']} vs Target</div>
            </div>
            """, unsafe_allow_html=True)

# MODULE 3: TPO SIMULATOR
elif st.session_state.current_page == "TPO Simulator":
    st.header("Trade Promo Optimizer")
    with st.container():
        st.selectbox("Retailer", ["Walmart", "Target", "Kroger"])
        st.slider("Discount Depth %", 5, 40, 15)
        st.button("Run Simulation", type="primary")

# MODULE 4: GEN AI ASSISTANT
elif st.session_state.current_page == "Gen AI Assistant":
    st.header("Gen AI Strategy Assistant")
    st.chat_message("assistant").write("Hello! I've analyzed the Reynolds dataset. How can I assist with your SKU profitability today?")
    st.chat_input("Show me top margin draggers...")
