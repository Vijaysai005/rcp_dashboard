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
# 2. CUSTOM CSS (Dark Sidebar / Light Main)
# ==========================================
st.markdown("""
<style>
    /* FORCE DARK SIDEBAR */
    [data-testid="stSidebar"] {
        background-color: #001529;
        color: white;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] span, [data-testid="stSidebar"] p {
        color: #ffffff !important;
    }
    /* Sidebar Nav Styling */
    div[data-testid="stRadio"] > label > div:first-child {
        display: none;
    }
    div[data-testid="stRadio"] label {
        color: white !important;
        font-size: 16px;
        padding: 10px;
        border-radius: 5px;
    }
    div[data-testid="stRadio"] label:hover {
        background-color: #1890ff;
        cursor: pointer;
    }
    
    /* MAIN CONTENT STYLING */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* CUSTOM METRIC CARDS */
    .metric-card {
        background-color: white;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        text-align: center;
    }
    
    /* TABLE HEADER COLOR */
    thead tr th:first-child {display:none}
    tbody th {display:none}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. BACKEND DUMMY DATA GENERATOR
# ==========================================
def get_dummy_data():
    # Simulating a CSV file load
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
# 4. UI COMPONENT FUNCTIONS
# ==========================================

def create_donut_chart(value, title, status_text, color):
    """Creates a Plotly gauge/donut chart similar to the mockup"""
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
            'steps': [
                {'range': [0, 100], 'color': "#f0f2f5"} # Grey background ring
            ],
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
        # Brand Header
        st.markdown("## **Reynolds**")
        st.markdown("<p style='color:#a6b1b7; margin-top:-15px; font-size:14px'>CPG Analytics Toolkit</p>", unsafe_allow_html=True)
        st.markdown("---")
        
        # Navigation
        selected = st.radio(
            "Navigation", 
            ["Data Management", "Unified Business Intelligence", "TPO Simulator", "Gen AI Assistant"],
            index=0
        )
        
        st.markdown("---")
        st.markdown(f"<p style='color:#5c6b7f; font-size:12px'>© 2026 Reynolds Consumer Products</p>", unsafe_allow_html=True)
        
        return selected

# ==========================================
# 5. MAIN APPLICATION LOGIC
# ==========================================

def main():
    module = render_sidebar()
    
    # ---------------------------------------------------------
    # MODULE 1: DATA MANAGEMENT (Default)
    # ---------------------------------------------------------
    if module == "Data Management":
        st.markdown("### Data Quality Scorecard")
        
        # -- Scorecard Row --
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
        
        # -- SKU Mapping Engine --
        st.markdown("### SKU Mapping Engine")
        
        # Controls
        col_search, col_filter = st.columns([3, 1])
        
        df = get_dummy_data()
        
        with col_search:
            search_query = st.text_input("🔍 Search by SKU, description, or retailer...", "")
            
        with col_filter:
            status_filter = st.selectbox("Filter Status", ["All", "Mapped", "Unmapped"])

        # Filtering Logic
        if status_filter != "All":
            df = df[df["Status"] == status_filter]
            
        if search_query:
            df = df[
                df["Product Description"].str.contains(search_query, case=False) | 
                df["Retailer SKU"].str.contains(search_query, case=False)
            ]

        # Stylized Data Table
        st.dataframe(
            df,
            column_config={
                "Retailer": st.column_config.TextColumn("RETAILER", width="small"),
                "Retailer SKU": st.column_config.TextColumn("RETAILER SKU", width="medium"),
                "Product Description": st.column_config.TextColumn("PRODUCT DESCRIPTION", width="large"),
                "SAP Material #": st.column_config.TextColumn("SAP MATERIAL #", width="medium"),
                "Status": st.column_config.TextColumn(
                    "STATUS", 
                    width="small",
                    help="Mapping status of the SKU"
                ),
                "Freshness": st.column_config.ProgressColumn(
                    "DATA HEALTH",
                    format="%f",
                    min_value=0,
                    max_value=100,
                ),
            },
            use_container_width=True,
            hide_index=True
        )

    # ---------------------------------------------------------
    # PLACEHOLDERS FOR OTHER MODULES
    # ---------------------------------------------------------
    elif module == "Unified Business Intelligence":
        st.info("🚧 Unified Business Intelligence module is currently under development.")
    elif module == "TPO Simulator":
        st.info("🚧 Trade Promotion Optimization Simulator is loading...")
    elif module == "Gen AI Assistant":
        st.info("💬 Gen AI Assistant is ready to chat.")

if __name__ == "__main__":
    main()
