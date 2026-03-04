import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import io

# --- 1. MOCK CPG DATA (CSV IO) ---
csv_raw = """Module,Category,Label,Value,Trend,Status,Retailer,SKU,Description,SAP_ID
DataMgmt,Quality,Nielsen POS,98,,Excellent,,,,
DataMgmt,Quality,Internal Shipments,100,,Excellent,,,,
DataMgmt,Quality,Trade Planner,85,,Good,,,,
DataMgmt,Quality,IRI Data,92,,Good,,,,
DataMgmt,Mapping,,,Walmart,WMT-RF-200,Reynolds Wrap 200sqft,1000234567,Mapped
DataMgmt,Mapping,,,Target,TGT-RF-075,Reynolds Wrap 75sqft,1000234568,Mapped
DataMgmt,Mapping,,,Kroger,KRO-HB-13G,Hefty Strong 13G,2000456789,Unmapped
BI,KPI,Market Share,23.4%,+1.2%,Positive,,,,
BI,KPI,Velocity,4.2,-0.3,Negative,,,,
BI,KPI,Gross Margin,34.8%,+2.1%,Positive,,,,
BI,KPI,Trade ROI,2.8x,+0.4x,Positive,,,,
"""

@st.cache_data
def get_cpg_data():
    return pd.read_csv(io.StringIO(csv_raw))

df = get_cpg_data()

# --- 2. THEME & UI STYLING ---
st.set_page_config(layout="wide", page_title="Reynolds Analytics")

st.markdown("""
<style>
    [data-testid="stSidebar"] { background-color: #0F172A; }
    .stButton > button {
        width: 100%; border: none; background-color: transparent; color: #94A3B8;
        text-align: left; padding: 12px; font-size: 15px; display: flex; align-items: center;
    }
    .stButton > button:hover { background-color: #1E293B; color: #38BDF8; }
    .active-nav button { background-color: #2563EB !important; color: white !important; border-radius: 8px; }
    
    .card { background: white; padding: 15px; border-radius: 12px; border: 1px solid #E2E8F0; text-align: center; }
    .pill { padding: 3px 10px; border-radius: 12px; font-size: 11px; font-weight: 700; }
    .pill-excellent { color: #10B981; background: #DCFCE7; }
    .pill-good { color: #D97706; background: #FEF3C7; }
</style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("<h2 style='color:white;'>Reynolds</h2><p style='color:#64748B; font-size:12px;'>Analytics Toolkit</p>", unsafe_allow_html=True)
    st.write("---")
    
    if 'page' not in st.session_state: st.session_state.page = "Data Management"
    
    for label in ["Data Management", "Unified BI", "TPO Simulator", "Gen AI Assistant"]:
        active = "active-nav" if st.session_state.page == label else ""
        st.markdown(f'<div class="{active}">', unsafe_allow_html=True)
        if st.button(f"👁️ {label}"):
            st.session_state.page = label
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- 4. MODULE ROUTING ---
if st.session_state.page == "Data Management":
    st.header("Data Quality Scorecard")
    
    # Gauges from CSV
    dq = df[df['Module'] == 'DataMgmt']
    dq_scores = dq[dq['Category'] == 'Quality']
    cols = st.columns(4)
    
    for i, (_, row) in enumerate(dq_scores.iterrows()):
        with cols[i]:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.write(f"**{row['Label']}**")
            
            fig = go.Figure(go.Pie(values=[row['Value'], 100-row['Value']], hole=.75, 
                                   marker_colors=["#10B981" if row['Value'] > 90 else "#F59E0B", "#F1F5F9"], 
                                   textinfo='none', hoverinfo='none'))
            fig.update_layout(showlegend=False, height=120, margin=dict(t=0,b=0,l=0,r=0),
                              annotations=}%", x=0.5, y=0.5, font_size=18, showarrow=False)])
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            
            p_class = "pill-excellent" if row['Status'] == "Excellent" else "pill-good"
            st.markdown(f'<span class="pill {p_class}">{row["Status"]}</span>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("### SKU Mapping Engine")
    map_df = dq[dq['Module'] == 'DataMgmt'].dropna(subset=['Retailer'])
    st.dataframe(map_df[['Retailer', 'SKU', 'Description', 'SAP_ID', 'Status']], use_container_width=True, hide_index=True)

elif st.session_state.page == "Unified BI":
    st.header("Enterprise KPI Scorecard")
    kpi_df = df[df['Module'] == 'BI']
    cols = st.columns(4)
    for i, (_, row) in enumerate(kpi_df.iterrows()):
        with cols[i]:
            color = "#10B981" if row['Status'] == "Positive" else "#EF4444"
            st.markdown(f"""
            <div class="card">
                <div style='color:#64748B; font-size:12px;'>{row['Label']}</div>
                <div style='font-size:24px; font-weight:700;'>{row['Value']}</div>
                <div style='color:{color}; font-size:14px;'>{row['Trend']}</div>
            </div>
            """, unsafe_allow_html=True)

else:
    st.info(f"{st.session_state.page} view is active. Connect SAP HANA to live-stream additional {st.session_state.page} datasets.")
