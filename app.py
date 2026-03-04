import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import io

# --- PAGE CONFIGURATION ---
st.set_page_config(layout="wide", page_title="Reynolds CPG Analytics Toolkit", page_icon="📊")

# --- CSV DATA INITIALIZATION (I/O) ---
# This simulates reading from physical CSV files using String I/O
csv_data = """Section,Category,Label,Value,Trend,Status,Subtext,Retailer,SKU,Description,SAP_ID
Scorecard,DataQuality,Nielsen POS,98,,Excellent,98% Verified,,,,,
Scorecard,DataQuality,Internal Shipments,100,,Excellent,100% Synced,,,,,
Scorecard,DataQuality,Trade Planner,85,,Good,85% Action Req,,,,,
Scorecard,DataQuality,IRI Data,92,,Good,92% Verified,,,,,
KPI,Financial,Market Share,23.4%,+1.2%,Positive,Target: 22.5%,,,,,
KPI,Financial,Velocity,4.2,-0.3,Negative,Target: 4.5,,,,,
KPI,Financial,Gross Margin,34.8%,+2.1%,Positive,Target: 33.0%,,,,,
KPI,Financial,Trade ROI,2.8x,+0.4x,Positive,Target: 2.5x,,,,,
Mapping,SKU,,,,,Walmart,WMT-RF-200-01,Reynolds Wrap Aluminum Foil 200sqft,1000234567,Mapped
Mapping,SKU,,,,,Target,TGT-RF-075-02,Reynolds Wrap Aluminum Foil 75sqft,1000234568,Mapped
Mapping,SKU,,,,,Kroger,KRO-HB-13G-01,Hefty Strong 13G Trash Bags,2000456789,Unmapped
Mapping,SKU,,,,,Amazon,AMZ-RF-200-05,Reynolds Wrap Aluminum Foil 200sqft,1000234567,Mapped
Mapping,SKU,,,,,Walmart,WMT-HB-30G-09,Hefty Ultra Strong 30G,2000987654,Mapped
Trend,Monthly,Jan,22.1,12000,11500,,,,,,
Trend,Monthly,Feb,22.5,13500,12800,,,,,,
Trend,Monthly,Mar,23.0,11800,12100,,,,,,
Trend,Monthly,Apr,22.8,14200,13900,,,,,,
Trend,Monthly,May,23.4,12900,13100,,,,,,
Trend,Monthly,Jun,23.2,11000,11200,,,,,,
"""

@st.cache_data
def get_data():
    return pd.read_csv(io.StringIO(csv_data))

df = get_data()

# --- CUSTOM CSS FOR BRANDED UI ---
st.markdown("""
<style>
    /* Dark Sidebar Design */
    [data-testid="stSidebar"] { background-color: #0F172A; border-right: 1px solid #1E293B; }
    
    /* Left Aligned Eye Icon Navigation */
    .stButton > button {
        width: 100%; border: none; background-color: transparent; color: #94A3B8;
        text-align: left; padding: 12px 15px; font-size: 15px; transition: 0.3s;
        display: flex; align-items: center; justify-content: flex-start;
    }
    .stButton > button:hover { background-color: #1E293B; color: #38BDF8; }
    
    /* Active State Highlight */
    .nav-active button { background-color: #2563EB !important; color: white !important; border-radius: 8px; font-weight: 600; }

    /* Component Styling */
    .gauge-container { background: white; padding: 15px; border-radius: 12px; border: 1px solid #E2E8F0; text-align: center; }
    .status-pill { padding: 2px 10px; border-radius: 12px; font-size: 11px; font-weight: 700; }
    .status-excellent { color: #10B981; background: #DCFCE7; }
    .status-good { color: #D97706; background: #FEF3C7; }
    
    .kpi-card { background: white; padding: 20px; border-radius: 12px; border: 1px solid #E2E8F0; }
    .trend-pos { color: #10B981; font-weight: bold; }
    .trend-neg { color: #EF4444; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("<h2 style='color:white; margin-bottom:0;'>Reynolds</h2><p style='color:#64748B; font-size:12px;'>CPG Analytics Toolkit</p>", unsafe_allow_html=True)
    st.write("---")
    
    if 'page' not in st.session_state: st.session_state.page = "Data Management"

    nav_items = {
        "Data Management": "👁️",
        "Unified Business Intelligence": "📊",
        "TPO Simulator": "🎯",
        "Gen AI Assistant": "💬"
    }

    for label, icon in nav_items.items():
        is_active = "nav-active" if st.session_state.page == label else ""
        st.markdown(f'<div class="{is_active}">', unsafe_allow_html=True)
        if st.button(f"{icon} {label}", key=f"nav_{label}"):
            st.session_state.page = label
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.sidebar.markdown("<br><br><br><br><p style='color:#475569; font-size:10px;'>© 2026 Reynolds Consumer Products</p>", unsafe_allow_html=True)

# --- MODULE 1: DATA MANAGEMENT ---
if st.session_state.page == "Data Management":
    st.header("Data Quality Scorecard")
    dq_rows = df[df['Category'] == 'DataQuality']
    cols = st.columns(4)
    
    for i, (_, row) in enumerate(dq_rows.iterrows()):
        with cols[i]:
            st.markdown('<div class="gauge-container">', unsafe_allow_html=True)
            st.write(f"**{row['Label']}**")
            
            color = "#10B981" if row['Value'] >= 95 else "#F59E0B"
            fig = go.Figure(go.Pie(values=[row['Value'], 100-row['Value']], hole=.75, marker_colors=[color, "#F1F5F9"], textinfo='none'))
            fig.update_layout(showlegend=False, height=130, margin=dict(t=0, b=0, l=0, r=0),
                              annotations=)}%", x=0.5, y=0.5, font_size=20, showarrow=False, font_weight='bold')])
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            
            pill_type = "status-excellent" if row['Status'] == 'Excellent' else "status-good"
            st.markdown(f'<span class="status-pill {pill_type}">{row["Status"]}</span>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br><h3>SKU Mapping Engine</h3>", unsafe_allow_html=True)
    c1, c2 = st.columns([3, 1])
    search = c1.text_input("🔍 Search by SKU, description, or retailer...", placeholder="Search...")
    map_filter = c2.selectbox("Status", ["All", "Mapped", "Unmapped"])
    
    map_df = df[df['Section'] == 'Mapping'][['Retailer', 'SKU', 'Description', 'SAP_ID', 'Status']]
    if search:
        map_df = map_df[map_df['Description'].str.contains(search, case=False)]
    if map_filter != "All":
        map_df = map_df[map_df['Status'] == map_filter]

    st.dataframe(map_df, use_container_width=True, hide_index=True)

# --- MODULE 2: UNIFIED BUSINESS INTELLIGENCE ---
elif st.session_state.page == "Unified Business Intelligence":
    st.header("Unified Business Intelligence")
    tab1, tab2, tab3 = st.tabs(["Enterprise KPI Scorecard", "Shipment to Shelf", "Profitability"])
    
    with tab1:
        kpi_rows = df[df['Section'] == 'KPI']
        cols = st.columns(4)
        for i, (_, row) in enumerate(kpi_rows.iterrows()):
            with cols[i]:
                trend_class = "trend-pos" if row['Status'] == 'Positive' else "trend-neg"
                st.markdown(f"""<div class="kpi-card">
                    <div style='color:#64748B; font-size:12px; font-weight:600;'>{row['Label'].upper()}</div>
                    <div style='font-size:28px; font-weight:700;'>{row['Value']} <span class='{trend_class}' style='font-size:14px;'>({row['Trend']})</span></div>
                    <div style='color:#94A3B8; font-size:11px;'>{row['Subtext']}</div>
                </div>""", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        trend_df = df[df['Section'] == 'Trend']
        fig = px.line(trend_df, x='Label', y='Value', title="12-Month Market Share Trend", markers=True)
        fig.update_layout(template="plotly_white", height=400, xaxis_title="Month", yaxis_title="Share %")
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("Supply Chain Alignment")
        fig_ship = go.Figure()
        fig_ship.add_trace(go.Bar(x=trend_df['Label'], y=trend_df['Trend'], name='Internal Shipments', marker_color='#1E3A8A'))
        fig_ship.add_trace(go.Scatter(x=trend_df['Label'], y=trend_df['Status'], name='POS Consumption', line=dict(color='#38BDF8', width=3)))
        fig_ship.update_layout(barmode='group', template='plotly_white')
        st.plotly_chart(fig_ship, use_container_width=True)

# --- MODULE 3: TPO SIMULATOR ---
elif st.session_state.page == "TPO Simulator":
    st.header("Promo Scenario Simulator")
    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown("### Simulation Inputs")
        st.selectbox("Select Retailer", ["Walmart", "Target", "Kroger"])
        st.selectbox("Select Product", ["Reynolds Wrap 200sqft", "Hefty Strong 13G"])
        st.slider("Discount Depth %", 0, 40, 15)
        st.button("Run Prediction", type="primary")
    with c2:
        st.markdown("### Scenario Results")
        st.info("Simulation predicts a **14% Volume Lift** with an estimated ROI of **1.8x**.")
        st.line_chart([100, 110, 130, 145, 140])

# --- MODULE 4: GEN AI ASSISTANT ---
elif st.session_state.page == "Gen AI Assistant":
    st.header("Gen AI Strategy Assistant")
    c1, c2 = st.columns([2, 1])
    with c1:
        st.chat_message("assistant").write("Hello! I've analyzed last month's data. **Aluminum Foil** margins are under pressure due to commodity shifts. How can I help?")
        st.chat_input("Show me top margin draggers at Kroger...")
    with c2:
        st.markdown("### Automated Insights")
        st.warning("⚠️ **Commodity Alert:** Aluminum costs up 3.2%")
        st.success("✅ **OOS Resolved:** Target inventory healthy")
        st.error("📉 **Share Drop:** -0.5% in Waste & Storage")

