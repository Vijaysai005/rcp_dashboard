import streamlit as st
import pandas as pd
import numpy as np
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
    /* Active Focus State */
    .stButton > button:focus {
        background-color: #2563EB !important;
        color: #FFFFFF !important;
        box-shadow: none;
    }

    /* Metric & Card Styling */
    div[data-testid="stMetric"] {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border: 1px solid #E2E8F0;
    }

    /* Filter Bar Styling */
    .filter-bar {
        background-color: #FFFFFF;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
        border: 1px solid #E2E8F0;
    }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE NAVIGATION ---
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'UBI' 

def nav_to(page):
    st.session_state.current_page = page

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("<h2 style='color:white; margin-bottom:0;'>Reynolds</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748B; margin-top:0;'>CPG Analytics Toolkit</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Navigation list (Data Management moved to bottom)
    st.button("📊  Unified Business Intelligence", on_click=nav_to, args=('UBI',))
    st.button("📈  TPO Simulator", on_click=nav_to, args=('TPO',))
    st.button("✨  Gen AI Assistant", on_click=nav_to, args=('AI',))
    st.markdown("<br><br>", unsafe_allow_html=True) # Separation for Data Management
    st.button("🗄️  Data Management", on_click=nav_to, args=('DM',))
    
    st.sidebar.markdown("---")
    st.sidebar.caption("© 2026 Reynolds Consumer Products")

# --- DONUT CHART COMPONENT ---
def draw_donut(label, value, color):
    remaining = 100 - value
    fig = go.Figure(data=[go.Pie(
        labels=[label, 'Remaining'],
        values=[value, remaining],
        hole=.75,
        marker_colors=[color, '#E2E8F0'],
        textinfo='none',
        showlegend=False,
        hoverinfo='label+percent'
    )])
    fig.add_annotation(text=f"<b>{value}%</b>", x=0.5, y=0.5, showarrow=False, font_size=20, font_color="#1E293B")
    fig.update_layout(
        title={'text': label, 'x': 0.5, 'xanchor': 'center', 'font': {'size': 16, 'color': '#64748B'}},
        height=220, margin=dict(l=10, r=10, t=50, b=10), paper_bgcolor="rgba(0,0,0,0)"
    )
    return fig

# --- MODULE CONTENT ---

# 1. UNIFIED BUSINESS INTELLIGENCE
if st.session_state.current_page == 'UBI':
    st.title("Unified Business Intelligence")
    
    # Page Filters
    f1, f2 = st.columns(2)
    retailer = f1.selectbox("Retailer", ["All Retailers", "Walmart", "Target", "Kroger", "CVS"], key="ubi_r")
    category = f2.selectbox("Product Category", ["All", "Aluminum Foil", "Trash Bags", "Plastic Wrap"], key="ubi_c")
    
    ubi_tabs = st.tabs(["Enterprise KPI Scorecard", "Shipment to Shelf", "SKU & Customer Profitability"])
    
    with ubi_tabs[0]:
        st.subheader(f"Performance Overview: {retailer}")
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Market Share", "23.4%", "1.2%", help="Target: 22.5%")
        k2.metric("Velocity", "4.2", "-0.3", help="Target: 4.5")
        k3.metric("Gross Margin", "34.8%", "2.1%", help="Target: 33.0%")
        k4.metric("Trade ROI", "2.8x", "0.4x", help="Target: 2.5x")
        
        st.subheader("12-Month Market Share Tracker")
        st.line_chart(pd.DataFrame(np.random.randn(12, 3), columns=['Reynolds', 'Competitor A', 'Private Label']))

    with ubi_tabs[1]:
        st.subheader("Inventory Health Matrix (Days of Supply)")
        dos_df = pd.DataFrame({
            "Retailer": ["Walmart", "Target", "Kroger", "CVS"],
            "Aluminum Foil": [18, 25, 12, 8],
            "Trash Bags": [22, 19, 16, 11],
            "Plastic Wrap": [15, 21, 14, 9]
        })
        st.table(dos_df.style.background_gradient(cmap='RdYlGn', subset=["Aluminum Foil", "Trash Bags", "Plastic Wrap"]))
        st.error("🚨 **OOS Risk**: Reynolds Wrap 200sqft at CVS is below 8 Days Supply (Critical).")

    with ubi_tabs[2]:
        st.subheader("Margin Waterfall")
        fig_wf = go.Figure(go.Waterfall(
            orientation = "v",
            measure = ["relative", "relative", "relative", "total"],
            x = ["Gross Revenue", "COGS", "Trade Spend", "Net Margin"],
            y = [100, -42, -18, 40],
            connector = {"line":{"color":"#cbd5e1"}}
        ))
        st.plotly_chart(fig_wf, use_container_width=True)

# 2. TPO SIMULATOR
elif st.session_state.current_page == 'TPO':
    st.title("TPO Simulator")
    
    # Page Filters
    f1, f2 = st.columns(2)
    f1.selectbox("Retailer", ["Walmart", "Target", "Kroger"], key="tpo_r")
    f2.selectbox("Product Line", ["Aluminum Foil", "Trash Bags"], key="tpo_c")
    
    sim_col1, sim_col2 = st.columns()
    with sim_col1:
        st.info("Promo Parameters")
        st.selectbox("Select Product SKU", ["Reynolds Wrap 200sqft", "Hefty Ultra Strong 30Gal"])
        st.selectbox("Discount Type", ["% Off", "TPR", "Display"])
        st.slider("Discount Amount (%)", 0, 50, 20)
        st.button("Run Simulation", type="primary", use_container_width=True)

    with sim_col2:
        st.subheader("Scenario Comparison")
        comp_df = pd.DataFrame({
            "Metric": ["Predicted Volume", "Predicted Revenue", "Promo Spend", "Predicted ROI"],
            "Baseline": ["42,000", "$168,000", "$0", "0.0x"],
            "Scenario 1 (Moderate)": ["56,700 (+35%)", "$208,656", "$28,000", "1.6x"],
            "Scenario 2 (Aggressive)": ["65,100 (+55%)", "$229,152", "$42,000", "0.9x"]
        })
        st.table(comp_df)
        st.success("✅ **Recommendation**: Scenario 1 offers the optimal balance of lift and margin.")

# 3. GEN AI ASSISTANT
elif st.session_state.current_page == 'AI':
    st.title("Gen AI NL Assistant")
    
    # Page Filters
    f1, f2 = st.columns(2)
    f1.selectbox("Retailer Context", ["All", "Walmart", "Target"], key="ai_r")
    f2.selectbox("Category Context", ["All", "Foil", "Waste"], key="ai_c")

    chat_col, alert_col = st.columns()
    with chat_col:
        st.chat_message("assistant").write("Hello! I'm your CPG Assistant. How can I help you analyze performance today?")
        st.text_input("Ask a natural language question...", placeholder="e.g., Show me margin draggers at Walmart")
        st.caption("Quick Tips: 'Market share trends' | 'Best promo ROI'")

    with alert_col:
        st.markdown("### Automated Insights")
        st.warning("**Commodity Alert**: Aluminum costs rose 3%, impacting foil margins.")
        st.info("**Retailer Trend**: Private Label foil share decreased by 0.5% at Kroger.")

# 4. DATA MANAGEMENT (Bottom of List)
elif st.session_state.current_page == 'DM':
    st.title("Data Management Portal")
    
    # Page Filters
    f1, f2 = st.columns(2)
    f1.selectbox("Source Retailer", ["All Retailers", "Walmart", "Target", "Kroger"], key="dm_r")
    f2.selectbox("Data Category", ["All Categories", "Aluminum Foil", "Trash Bags"], key="dm_c")

    st.subheader("Data Quality Scorecard")
    d1, d2, d3, d4 = st.columns(4)
    # Using Colorful Donut Charts
    d1.plotly_chart(draw_donut("Nielsen POS", 98, "#10B981"), use_container_width=True) # Green
    d2.plotly_chart(draw_donut("Internal Shipments", 100, "#3B82F6"), use_container_width=True) # Blue
    d3.plotly_chart(draw_donut("Trade Planner", 85, "#F59E0B"), use_container_width=True) # Amber
    d4.plotly_chart(draw_donut("IRI Data", 92, "#8B5CF6"), use_container_width=True) # Purple

    st.markdown("---")
    st.subheader("SKU Mapping Engine")
    s1, s2 = st.columns(2)
    s1.text_input("Search by SKU or SAP #")
    s2.selectbox("Mapping Status", ["All", "Mapped", "Unmapped"])
    
    mapping_data = pd.DataFrame({
        "Retailer": ["Walmart", "Target", "Kroger", "CVS", "Walmart"],
        "Retailer SKU": ["WMT-RF-200-01", "TGT-TB-30-50", "KRG-PW-100", "CVS-AF-75", "WMT-P-50"],
        "Product Description": ["Reynolds Wrap Aluminum Foil 200sqft", "Hefty Ultra Strong 30Gal", "Reynolds Plastic Wrap 100sqft", "Reynolds Foil 75sqft", "Reynolds Parchment 50sqft"],
        "SAP Material #": ["1000234567", "1000987654", "1000556677", "1000334455", "1000112233"],
        "Status": ["Mapped", "Mapped", "Unmapped", "Mapped", "Mapped"]
    })
    st.dataframe(mapping_data, use_container_width=True, hide_index=True)
