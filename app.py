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
    
    /* Left-aligned Sidebar Buttons with Active State */
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
    .stButton > button:focus, .stButton > button:active {
        background-color: #2563EB !important;
        color: #FFFFFF !important;
        box-shadow: none;
    }

    /* Professional Headers */
    h1, h2, h3 { color: #1E293B; font-family: 'Inter', sans-serif; }
    
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

# --- SESSION STATE FOR NAVIGATION ---
if 'page' not in st.session_state:
    st.session_state.page = 'Data Management'

def set_page(page_name):
    st.session_state.page = page_name

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color:white; margin-bottom:0;'>Reynolds</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748B; margin-top:0;'>CPG Analytics Toolkit</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🗄️  Data Management"): set_page('Data Management')
    if st.button("📊  Unified Business Intelligence"): set_page('UBI')
    if st.button("📈  TPO Simulator"): set_page('TPO')
    if st.button("✨  Gen AI Assistant"): set_page('AI')
    
    st.sidebar.markdown("---")
    st.sidebar.caption("© 2026 Reynolds Consumer Products")

# --- GAUGE COMPONENT FUNCTION ---
def draw_gauge(label, value, color="#2563EB"):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = value,
        title = {'text': label, 'font': {'size': 18}},
        gauge = {
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "#E2E8F0",
            'steps': [
                {'range': [0, 70], 'color': '#FEE2E2'},
                {'range': [70, 90], 'color': '#FEF3C7'},
                {'range': [90, 100], 'color': '#DCFCE7'}],
        }
    ))
    fig.update_layout(height=200, margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor="rgba(0,0,0,0)")
    return fig

# --- MODULE 1: DATA MANAGEMENT ---
if st.session_state.page == 'Data Management':
    st.title("Data Management Portal")
    
    st.subheader("Data Quality Scorecard")
    g1, g2, g3, g4 = st.columns(4)
    with g1: st.plotly_chart(draw_gauge("Nielsen POS", 98, "#10B981"), use_container_width=True)
    with g2: st.plotly_chart(draw_gauge("Internal Shipments", 100, "#10B981"), use_container_width=True)
    with g3: st.plotly_chart(draw_gauge("Trade Planner", 85, "#F59E0B"), use_container_width=True)
    with g4: st.plotly_chart(draw_gauge("IRI Data", 92, "#10B981"), use_container_width=True)
    
    st.markdown("---")
    st.subheader("SKU Mapping Engine")
    col_f1, col_f2 = st.columns([2, 1])
    search = col_f1.text_input("🔍 Search by SKU, description, or retailer...", placeholder="e.g. WMT-RF-200")
    status_filter = col_f2.selectbox("Status", ["All", "Mapped", "Unmapped"])
    
    mapping_df = pd.DataFrame({
        "Retailer": ["Walmart", "Target", "Kroger", "CVS", "Walmart", "Kroger"],
        "Retailer SKU": ["WMT-RF-200-01", "TGT-TB-30-50", "KRG-PW-100", "CVS-AF-75", "WMT-P-50", "KRG-F-12"],
        "Product Description": ["Reynolds Wrap Aluminum Foil 200sqft", "Hefty Ultra Strong 30Gal", "Reynolds Plastic Wrap 100sqft", "Reynolds Foil 75sqft", "Reynolds Parchment 50sqft", "Reynolds Foil 12sqft"],
        "SAP Material #": ["1000234567", "1000987654", "1000556677", "1000334455", "1000112233", "Pending"],
        "Status": ["Mapped", "Mapped", "Unmapped", "Mapped", "Mapped", "Unmapped"]
    })
    st.dataframe(mapping_df, use_container_width=True, hide_index=True)

# --- MODULE 2: UNIFIED BUSINESS INTELLIGENCE ---
elif st.session_state.page == 'UBI':
    st.title("Unified Business Intelligence")
    ubi_tabs = st.tabs(["Enterprise KPI Scorecard", "Shipment to Shelf", "SKU & Customer Profitability"])
    
    with ubi_tabs[0]:
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Market Share", "23.4%", "1.2%", help="Target: 22.5%")
        k2.metric("Velocity", "4.2", "-0.3", help="Target: 4.5")
        k3.metric("Gross Margin", "34.8%", "2.1%", help="Target: 33.0%")
        k4.metric("Trade ROI", "2.8x", "0.4x", help="Target: 2.5x")
        
        st.subheader("Market Share Tracker (12 Month)")
        st.line_chart(np.random.randn(12, 3) + [24, 19, 16])

    with ubi_tabs[1]:
        st.subheader("Inventory Health Matrix (Days of Supply)")
        dos_data = pd.DataFrame({
            "Retailer": ["Walmart", "Target", "Kroger", "CVS"],
            "Aluminum Foil": [18, 25, 12, 8],
            "Trash Bags": [22, 19, 16, 11],
            "Plastic Wrap": [15, 21, 14, 9]
        })
        st.table(dos_data.style.background_gradient(cmap='RdYlGn', subset=["Aluminum Foil", "Trash Bags", "Plastic Wrap"]))
        st.error("🚨 **OOS Risk Alert**: Reynolds Wrap 200sqft at CVS (8 Days Supply) - Critical Risk Level")

    with ubi_tabs[2]:
        st.subheader("Margin Waterfall")
        # Simplified representation of the waterfall logic
        st.image("https://upload.wikimedia.org", width=700) # Placeholder
        st.caption("Waterfall details: Gross Sales -> COGS -> Trade Spend -> Net Margin")

# --- MODULE 3: TPO SIMULATOR (UPDATED TO MATCH PDF) ---
# --- MODULE 3: TPO SIMULATOR (HIGH-FIDELITY REALISTIC) ---
elif st.session_state.page == 'TPO':
    st.title("📈 TPO Simulator")
    st.markdown("Model promotional scenarios and predict volume lift, revenue, and ROI")
    
    # --- TOP ROW: INPUT PARAMETERS ---
    with st.container(border=True):
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1: retailer = st.selectbox("Retailer", ["Walmart", "Target", "Kroger", "CVS"], index=0)
        with col2: product = st.selectbox("Product", ["Reynolds Wrap 200sqft", "Hefty Ultra Strong 30Gal"], index=0)
        with col3: disc_type = st.selectbox("Discount Type", ["% Off", "BOGO", "TPR"], index=0)
        with col4: disc_amt = st.number_input("Discount Amount (%)", value=20, step=5)
        with col5: duration = st.number_input("Duration (weeks)", value=2, step=1)
        
        st.button("Run Simulation", type="primary", use_container_width=True)

    # --- MIDDLE ROW: KPI CARDS (DYNAMICS SIMULATION) ---
    # Realistic calculations based on PDF data points
    baseline_vol = 42000
    baseline_rev = 168000
    baseline_margin = 58800

    # Scenario 1 (Moderate - 20% Off)
    s1_vol = int(baseline_vol * 1.35) # +35% lift
    s1_rev = 208656
    s1_margin = 45030
    s1_roi = 1.6

    # Scenario 2 (Aggressive - 30% Off)
    s2_vol = int(baseline_vol * 1.55) # +55% lift
    s2_rev = 229152
    s2_margin = 38203
    s2_roi = 0.9

    st.markdown("### Simulation Summary")
    kpi1, kpi2, kpi3 = st.columns(3)

    with kpi1:
        st.markdown("<div style='background-color:#F1F5F9; padding:15px; border-radius:10px; border-left: 5px solid #94A3B8;'><strong>Baseline</strong><br><small>No Promotion</small></div>", unsafe_allow_html=True)
        st.metric("Volume", f"{baseline_vol:,}")
        st.metric("Revenue", f"${baseline_rev:,}")
        st.metric("Net Margin", f"${baseline_margin:,}")

    with kpi2:
        st.markdown("<div style='background-color:#EFF6FF; padding:15px; border-radius:10px; border-left: 5px solid #3B82F6;'><strong>Scenario 1: Moderate</strong><br><small>20% Discount</small></div>", unsafe_allow_html=True)
        st.metric("Volume", f"{s1_vol:,}", "+35%")
        st.metric("Revenue", f"${s1_rev:,}", "+24%")
        st.metric("Net Margin", f"${s1_margin:,}", "-23%", delta_color="inverse")
        st.markdown(f"<h2 style='color:#10B981; margin-top:0;'>ROI: {s1_roi}x</h2>", unsafe_allow_html=True)

    with kpi3:
        st.markdown("<div style='background-color:#F5F3FF; padding:15px; border-radius:10px; border-left: 5px solid #8B5CF6;'><strong>Scenario 2: Aggressive</strong><br><small>30% Discount</small></div>", unsafe_allow_html=True)
        st.metric("Volume", f"{s2_vol:,}", "+55%")
        st.metric("Revenue", f"${s2_rev:,}", "+36%")
        st.metric("Net Margin", f"${s2_margin:,}", "-35%", delta_color="inverse")
        st.markdown(f"<h2 style='color:#EF4444; margin-top:0;'>ROI: {s2_roi}x</h2>", unsafe_allow_html=True)

    # --- BOTTOM ROW: GRAPH & RECOMMENDATION ---
    st.markdown("---")
    g_col, r_col = st.columns([2, 1])

    with g_col:
        st.subheader("Scenario Comparison")
        # Realistic multi-metric chart from PDF
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Baseline', x=['Volume', 'Revenue'], y=[baseline_vol, baseline_rev], marker_color='#94A3B8'))
        fig.add_trace(go.Bar(name='Scenario 1', x=['Volume', 'Revenue'], y=[s1_vol, s1_rev], marker_color='#3B82F6'))
        fig.add_trace(go.Bar(name='Scenario 2', x=['Volume', 'Revenue'], y=[s2_vol, s2_rev], marker_color='#8B5CF6'))
        
        fig.update_layout(barmode='group', height=300, margin=dict(t=0, b=0, l=0, r=0), 
                          paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig, use_container_width=True)

    with r_col:
        st.subheader("Recommendation")
        st.success(f"""
        **Scenario 1 (Moderate)** offers the best balance of volume lift and ROI at **1.6x**.  
        
        *   **Volume Lift:** +35%  
        *   **Net Margin:** ${s1_margin:,}  
        *   **Efficiency:** High  
        """)
        st.info("💡 **Insight**: Scenario 2 provides higher volume but drops ROI below the 1.0x break-even threshold due to trade spend.")

# --- MODULE 4: GEN AI ASSISTANT ---
elif st.session_state.page == 'AI':
    st.title("✨ Gen AI NL Assistant")
    
    # Initialize chat history if it doesn't exist
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I'm your CPG Analytics Assistant. I can help you analyze data, identify trends, and answer questions about Reynolds products. What would you like to know?"}
        ]

    ai_left, ai_right = st.columns([2, 1])

    with ai_left:
        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # React to user input
        if prompt := st.chat_input("Ask a question about your CPG data..."):
            # Display user message in chat message container
            st.chat_message("user").markdown(prompt)
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})

            # --- MOCK LOGIC FOR RESPONSES ---
            response = "I'm analyzing that for you..."
            
            if "margin draggers" in prompt.lower():
                response = """Based on last month's data at **Walmart**, the top 3 margin draggers are:
                1. **Reynolds Wrap 200sqft**: -2.1% (High promo depth)
                2. **Hefty Ultra Strong 30Gal**: -1.5% (Logistics cost spike)
                3. **Reynolds Foil 75sqft**: -0.8% (Commodity price impact)"""
            
            elif "roi" in prompt.lower():
                response = "The best promo ROI currently is **1.6x** for the 'Moderate' scenario on Reynolds Wrap 200sqft at Walmart."
            
            elif "market share" in prompt.lower():
                response = "Current Market Share is **23.4%**, which is **+1.2%** above the target of 22.5%."

            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                st.markdown(response)
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})


    with ai_right:
        if st.button("Clear Chat History"):
            st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I help you today?"}]
            st.rerun()
        
        st.subheader("Automated Insights")
        
        # Commodity Alert Styled Card
        st.warning("""
        **⚠️ Commodity Cost Alert**  
        Aluminum commodity costs rose 3%, impacting foil margins.  
        *Expected Q2 impact: -$1.2M*
        """)
        
        st.info("""
        **💡 Quick Questions**  
        - Top margin draggers  
        - Market share trends  
        - Best promo ROI
        """)

    with ai_right:
        st.subheader("💡 Context & Insights")
        
        # 1. Data Source Indicators
        st.markdown("**Data Sources Active**")
        st.checkbox("Nielsen POS (Wk 40)", value=True)
        st.checkbox("Internal Shipments (Wk 40)", value=True)
        st.checkbox("Trade Planner", value=True)
        
        st.markdown("---")
        
        # 2. Key Insights Panel
        st.markdown("**Top Insights**")
        with st.expander("🚨 OOS Risk: CVS", expanded=True):
            st.caption("Reynolds Wrap 200sqft at CVS is at 8 Days Supply.")
            
        with st.expander("📈 Best Promo ROI", expanded=True):
            st.caption("Target TGT-TB-30-50 shows 2.2x ROI (Moderate Discount).")

        # 3. Suggested Prompts
        st.markdown("---")
        st.markdown("**Try asking:**")
        st.markdown("- *Show me top 5 margin draggers at Walmart last month*")
        st.markdown("- *Compare ROI: BOGO vs % Off on Foil*")
