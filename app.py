import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import io

# ==========================================
# 1. PAGE CONFIGURATION & THEME
# ==========================================
st.set_page_config(
    page_title="Reynolds CPG Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. CUSTOM CSS (Final UI Fixes)
# ==========================================
st.markdown("""
<style>
    /* FORCE DARK SIDEBAR */
    [data-testid="stSidebar"] {
        background-color: #001529 !important;
    }
    
    /* LEFT ALIGN SIDEBAR CONTENT */
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        align-items: flex-start !important;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
    }

    /* LOGO STYLING */
    .sidebar-logo {
        width: 180px;
        filter: brightness(0) invert(1); 
        margin-bottom: 10px;
    }

    /* FIX BUTTON VISIBILITY & LEFT ALIGNMENT */
    [data-testid="stSidebar"] .stButton button {
        text-align: left !important;
        justify-content: flex-start !important;
        padding-left: 15px !important;
        display: flex !important;
        width: 100% !important;
        /* Force dark text for visibility on white unselected buttons */
        color: #333333 !important; 
        background-color: #ffffff !important;
        border: 1px solid rgba(0,0,0,0.1) !important;
    }

    /* Ensure text inside button spans is also dark */
    [data-testid="stSidebar"] .stButton button p {
        color: #333333 !important;
        text-align: left !important;
    }

    /* SELECTED (PRIMARY) BUTTON STYLING */
    [data-testid="stSidebar"] .stButton button[kind="primary"] {
        background-color: #FF4B4B !important;
        color: white !important;
        border: none !important;
    }
    
    [data-testid="stSidebar"] .stButton button[kind="primary"] p {
        color: white !important;
    }

    /* HEADER TEXT COLOR */
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] p {
        color: #ffffff !important;
        text-align: left !important;
    }
    
    /* MAIN CONTENT STYLING */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* TABLE HEADER COLOR */
    thead tr th:first-child {display:none}
    tbody th {display:none}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. SESSION STATE MANAGEMENT
# ==========================================
if "selected_module" not in st.session_state:
    st.session_state.selected_module = "Data Management"

def set_page(page_name):
    st.session_state.selected_module = page_name

# ==========================================
# 4. BACKEND DUMMY DATA GENERATOR
# ==========================================
def get_dummy_data():
    csv_data = """Retailer,Retailer SKU,Product Description,SAP Material #,Status,Freshness
Walmart,WMT-RF-200-01,Reynolds Wrap Aluminum Foil 200sqft,1000234567,Mapped,99%
Target,TGT-HF-TR-13G,Hefty Ultra Strong Trash Bags 13 Gal,1000239988,Mapped,100%
Kroger,KRO-PL-WR-100,Reynolds Kitchens Plastic Wrap 100sqft,1000231122,Unmapped,85%
Costco,CST-RF-HD-500,Reynolds Wrap Heavy Duty 500sqft,,Unmapped,90%
Amazon,AMZ-PARCH-50,Reynolds Kitchens Parchment Paper,1000237744,Mapped,98%
Sam's Club,SAM-HEFTY-L,Hefty Large Black Trash Bags 30 Gal,1000235566,Mapped,100%
Publix,PUB-SLOW-CK,Reynolds Slow Cooker Liners 6ct,,Unmapped,80%
Walmart,WMT-WAX-75,Reynolds Cut-Rite Wax Paper,1000233344,Mapped,95%
"""
    return pd.read_csv(io.StringIO(csv_data))

# ==========================================
# 5. UI COMPONENT FUNCTIONS
# ==========================================
def create_donut_chart(value, title, status_text, color):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = value,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': title, 'font': {'size': 14, 'color': "#666"}},
        number = {'suffix': "%", 'font': {'size': 24, 'color': "#333"}},
        gauge = {
            'axis': {'range': [None, 100], 'visible': False},
            'bar': {'color': color},
            'bgcolor': "white",
            'borderwidth': 0,
            'bordercolor': "white",
            'steps': [{'range': [0, 100], 'color': "#f0f2f5"}],
        }
    ))
    fig.update_layout(
        height=160, 
        margin={'t': 40, 'b': 10, 'l': 20, 'r': 20},
        paper_bgcolor='rgba(0,0,0,0)',
        font={'family': "Arial"}
    )
    return fig

def render_sidebar():
    with st.sidebar:
        # Reynolds Logo 
        st.markdown('<img src="https://www.reynoldsconsumerproducts.com" class="sidebar-logo">', unsafe_allow_html=True)
        st.markdown("## **Reynolds**")
        st.markdown("<p style='color:#a6b1b7; margin-top:-15px; font-size:14px'>CPG Analytics Toolkit</p>", unsafe_allow_html=True)
        st.markdown("---")
        
        # NAVIGATION BUTTONS
        if st.button("📁 Data Management", use_container_width=True, type="primary" if st.session_state.selected_module == "Data Management" else "secondary"):
            set_page("Data Management")
            
        if st.button("📊 Unified Business Intelligence", use_container_width=True, type="primary" if st.session_state.selected_module == "Unified Business Intelligence" else "secondary"):
            set_page("Unified Business Intelligence")
            
        if st.button("🎯 TPO Simulator", use_container_width=True, type="primary" if st.session_state.selected_module == "TPO Simulator" else "secondary"):
            set_page("TPO Simulator")
            
        if st.button("💬 Gen AI Assistant", use_container_width=True, type="primary" if st.session_state.selected_module == "Gen AI Assistant" else "secondary"):
            set_page("Gen AI Assistant")

        st.markdown("---")
        st.markdown(f"<p style='color:#5c6b7f; font-size:12px'>© 2026 Reynolds Consumer Products</p>", unsafe_allow_html=True)

# ==========================================
# 6. MAIN APPLICATION LOGIC
# ==========================================
def main():
    render_sidebar()
    module = st.session_state.selected_module
    
    if module == "Data Management":
        st.markdown("### Data Quality Scorecard")
        c1, c2, c3, c4 = st.columns(4)
        
        with c1:
            st.plotly_chart(create_donut_chart(98, "Nielsen POS", "Excellent", "#00C49F"), use_container_width=True)
            st.markdown("<div style='text-align:center; color:#00C49F; font-weight:bold; margin-top:-10px'>Excellent</div>", unsafe_allow_html=True)
            
        with c2:
            st.plotly_chart(create_donut_chart(100, "Internal Shipments", "Excellent", "#00C49F"), use_container_width=True)
            st.markdown("<div style='text-align:center; color:#00C49F; font-weight:bold; margin-top:-10px'>Excellent</div>", unsafe_allow_html=True)

        with c3:
            st.plotly_chart(create_donut_chart(85, "Trade Planner", "Good", "#FFBB28"), use_container_width=True)
            st.markdown("<div style='text-align:center; color:#FFBB28; font-weight:bold; margin-top:-10px'>Good</div>", unsafe_allow_html=True)

        with c4:
            st.plotly_chart(create_donut_chart(92, "IRI Data", "Good", "#00C49F"), use_container_width=True)
            st.markdown("<div style='text-align:center; color:#00C49F; font-weight:bold; margin-top:-10px'>Good</div>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### SKU Mapping Engine")
        col_search, col_filter = st.columns([3, 1])
        df = get_dummy_data()
        with col_search:
            search_query = st.text_input("🔍 Search by SKU, description, or retailer...", "")
        with col_filter:
            status_filter = st.selectbox("Filter Status", ["All", "Mapped", "Unmapped"])

        if status_filter != "All":
            df = df[df["Status"] == status_filter]
        if search_query:
            df = df[df["Product Description"].str.contains(search_query, case=False) | df["Retailer SKU"].str.contains(search_query, case=False)]

        st.dataframe(df, use_container_width=True, hide_index=True)

if __name__ == "__main__":
    main()
