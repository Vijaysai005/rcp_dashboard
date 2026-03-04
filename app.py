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
        # --- 1. PAGE LEVEL FILTERS ---
        with st.container(border=True):
            c1, c2, c3 = st.columns(3)
            with c1: sel_bu = st.selectbox("Business Unit", ["All", "Cooking & Baking", "Tableware", "Waste Management"])
            with c2: sel_ret_kpi = st.selectbox("Retailer View", ["Total Market", "Walmart", "Target", "Kroger", "CVS"])
            with c3: sel_time = st.select_slider("Timeframe", options=["L13W", "L26W", "L52W/YTD"])

        # --- 2. DATA ENGINE (Reactive Logic) ---
        # Mock data mapping to show shifts when retailer/BU changes
        data_map = {
            "Total Market": {"ms": 23.4, "ms_d": "1.2%", "vel": 4.2, "gm": "34.8%", "roi": "2.8x"},
            "Walmart":      {"ms": 28.5, "ms_d": "2.1%", "vel": 4.8, "gm": "36.2%", "roi": "3.1x"},
            "Target":       {"ms": 19.8, "ms_d": "0.5%", "vel": 4.0, "gm": "33.5%", "roi": "2.6x"},
            "Kroger":       {"ms": 21.2, "ms_d": "-0.5%", "vel": 3.9, "gm": "32.5%", "roi": "2.4x"},
            "CVS":          {"ms": 12.4, "ms_d": "-1.1%", "vel": 3.2, "gm": "30.1%", "roi": "1.8x"}
        }
        
        # Get active data based on filter
        active = data_map.get(sel_ret_kpi, data_map["Total Market"])

        # --- 3. KEY PERFORMANCE INDICATORS ---
        st.markdown("### Key Performance Indicators")
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Market Share", f"{active['ms']}%", active['ms_d'], help="Target: 22.5%")
        k2.metric("Velocity", active['vel'], "-0.3", help="Target: 4.5")
        k3.metric("Gross Margin", active['gm'], "2.1%", help="Target: 33.0%")
        k4.metric("Trade ROI", active['roi'], "0.4x", help="Target: 2.5x")

        st.markdown("---")

        # --- 4. BRAND & BU SCORECARD (Filtered by Business Unit) ---
        st.markdown(f"### Brand & BU Scorecard: {sel_ret_kpi}")
        bu_data = pd.DataFrame({
            "BUSINESS UNIT": ["Cooking & Baking", "Tableware", "Waste Management", "Food Storage"],
            "MARKET SHARE": ["28.5%", "18.2%", "22.1%", "24.8%"],
            "VELOCITY": ["4.8", "3.9", "4.1", "4.0"],
            "GROSS MARGIN": ["36.2%", "31.5%", "33.8%", "34.1%"],
            "TRADE ROI": ["3.1x", "2.4x", "2.7x", "2.9x"]
        })
        
        # Filter the dataframe if a specific BU is selected
        if sel_bu != "All":
            filtered_bu = bu_data[bu_data["BUSINESS UNIT"] == sel_bu]
        else:
            filtered_bu = bu_data

        def highlight_cooking(s):
            return ['background-color: #F1F5F9; font-weight: bold' if s.name == 0 else '' for _ in s]
        
        st.table(filtered_bu.style.apply(highlight_cooking, axis=1))

        st.markdown("---")

        # --- 5. MARKET SHARE TRACKER (12 Month Graph - Reactive with Competitors) ---
        st.markdown(f"### {sel_ret_kpi} Market Share Tracker (12 Month)")
        months = ["Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Jan", "Feb"]
        
        # Adjusting baselines based on selected retailer's market share
        reynolds_base = active['ms']
        pl_base = 19.0  # Private Label average from PDF
        comp_base = 16.5 # Competitor average from PDF
        
        fig_ms = go.Figure()

        # Line 1: Reynolds (Primary - Blue)
        fig_ms.add_trace(go.Scatter(
            x=months, 
            y=[reynolds_base + np.random.uniform(-0.8, 0.8) for _ in range(12)], 
            name="Reynolds", 
            line=dict(color="#2563EB", width=4),
            mode='lines+markers'
        ))
        
        # Line 2: Private Label (Reference - Grey Dashed)
        fig_ms.add_trace(go.Scatter(
            x=months, 
            y=[pl_base + np.random.uniform(-0.5, 0.5) for _ in range(12)], 
            name="Private Label", 
            line=dict(color="#94A3B8", width=2, dash='dash'),
            mode='lines'
        ))

        # Line 3: Competitor A (New - Amber)
        fig_ms.add_trace(go.Scatter(
            x=months, 
            y=[comp_base + np.random.uniform(-0.7, 0.7) for _ in range(12)], 
            name="Competitor A", 
            line=dict(color="#F59E0B", width=2),
            mode='lines+markers'
        ))

        fig_ms.update_layout(
            hovermode="x unified",
            height=400,
            yaxis=dict(title="Share %", range=[0, 35], gridcolor='#F1F5F9'),
            xaxis=dict(gridcolor='#F1F5F9'),
            margin=dict(t=20, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor="white"
        )
        
        st.plotly_chart(fig_ms, use_container_width=True)

    with ubi_tabs[1]:
        # 1. PAGE LEVEL FILTERS (Reactive)
        with st.container(border=True):
            f1, f2 = st.columns(2)
            with f1: sel_retailer_ubi = st.selectbox("Filter by Retailer", ["All", "Walmart", "Target", "Kroger", "CVS"], key="ubi_ret")
            with f2: sel_cat_ubi = st.selectbox("Filter by Category", ["All", "Aluminum Foil", "Trash Bags", "Plastic Wrap", "Cookware"], key="ubi_cat")

        # 2. INVENTORY HEALTH MATRIX (Data from PDF)
        st.subheader("Inventory Health Matrix (Days of Supply)")
        dos_data = pd.DataFrame({
            "RETAILER": ["Walmart", "Target", "Kroger", "CVS"],
            "Aluminum Foil": [18, 25, 12, 8],
            "Trash Bags": [22, 19, 16, 11],
            "Plastic Wrap": [15, 21, 14, 9],
            "Cookware": [28, 32, 24, 19]
        })

        # Apply filtering for display
        display_dos = dos_data if sel_retailer_ubi == "All" else dos_data[dos_data["RETAILER"] == sel_retailer_ubi]
        
        def color_dos(val):
            if isinstance(val, (int, float)):
                if val < 10: return 'background-color: #FEE2E2; color: #991B1B; font-weight: bold' # Critical
                if val <= 15: return 'background-color: #FEF3C7; color: #92400E' # Low
                return 'background-color: #DCFCE7; color: #166534' # Healthy
            return ''

        st.table(display_dos.style.applymap(color_dos, subset=["Aluminum Foil", "Trash Bags", "Plastic Wrap", "Cookware"]))

        col_left, col_right = st.columns([2, 1])

        # 3. INTERNAL SHIPMENTS vs POS (Visualized from PDF)
        with col_left:
            st.subheader("Internal Shipments vs POS Consumption")
            # Realistic fluctuating data based on the PDF chart
            weeks = [f"W{i}" for i in range(1, 9)]
            shipments = [42000, 45000, 48000, 43000, 52000, 46000, 49000, 47000]
            pos_cons = [38000, 41000, 43000, 40000, 44000, 47000, 45000, 48000]
            
            fig_sync = go.Figure()
            fig_sync.add_trace(go.Bar(x=weeks, y=shipments, name="Internal Shipments", marker_color="#3B82F6", opacity=0.8))
            fig_sync.add_trace(go.Scatter(x=weeks, y=pos_cons, name="POS Consumption", line=dict(color="#10B981", width=4), mode='lines+markers'))
            fig_sync.update_layout(height=350, margin=dict(t=10, b=10), legend=dict(orientation="h", y=1.1))
            st.plotly_chart(fig_sync, use_container_width=True)

        # 4. OOS RISK RADAR (Data from PDF)
        with col_right:
            st.subheader("OOS Risk Radar")
            oos_data = pd.DataFrame({
                "SKU": ["Reynolds Wrap 200sqft", "Hefty Ultra Strong 30Gal", "Reynolds Parchment 50sqft"],
                "RETAILER": ["Kroger", "CVS", "Walmart"],
                "DOS": [8, 9, 12],
                "VELOCITY": ["High", "High", "Medium"],
                "RISK": ["CRITICAL", "CRITICAL", "WARNING"]
            })

            # Filter logic for the Radar
            filtered_oos = oos_data
            if sel_retailer_ubi != "All":
                filtered_oos = oos_data[oos_data["RETAILER"] == sel_retailer_ubi]
            
            if filtered_oos.empty:
                st.success("✅ No critical OOS risks for selected filters.")
            else:
                for idx, row in filtered_oos.iterrows():
                    color = "red" if row['RISK'] == "CRITICAL" else "orange"
                    st.info(f"**{row['SKU']}** ({row['RETAILER']})\n\n"
                            f"Status: :{color}[{row['RISK']}] | {row['DOS']} Days Supply")


    with ubi_tabs[2]:
       # 1. PAGE LEVEL FILTERS
       with st.container(border=True):
           f1, f2, f3 = st.columns(3)
           with f1: sel_retailer = st.selectbox("Select Retailer", ["Walmart", "Target", "Kroger", "CVS"], index=0)
           with f2: sel_product = st.selectbox("Select Category", ["Aluminum Foil", "Trash Bags", "Plastic Wrap"], index=0)
           with f3: sel_period = st.select_slider("Timeframe", options=["L3M", "L6M", "YTD"])

       # 2. REACTIVE DATA ENGINE (Mocks the Reynolds Database)
       # Different data profiles for different retailers to show "reaction"
       data_profiles = {
           "Walmart": {"vol": [12, -2, 8, 15], "margin": [42, 18, 35, 38], "wf": [100, -28, -32, -12, 28]},
           "Target":  {"vol": [5, 10, -5, 2], "margin": [35, 45, 22, 28], "wf": [100, -22, -35, -10, 33]},
           "Kroger":  {"vol": [-8, 4, 12, -2], "margin": [15, 32, 48, 25], "wf": [100, -35, -30, -15, 20]},
           "CVS":     {"vol": [2, -12, 3, 20], "margin": [28, 12, 31, 52], "wf": [100, -15, -40, -10, 35]}
       }
       
       profile = data_profiles[sel_retailer]
       sku_names = [f"{sel_product} 200ft", f"{sel_product} 75ft", "Hefty 30G", "Parchment 50ft"]

       # 3. DRIVERS & DRAGGERS MATRIX
       st.subheader(f"Drivers & Draggers: {sel_retailer} {sel_product}")
       
       # Determine color based on quadrants (Top-Right = Green, Bottom-Left = Red)
       colors = []
       for v, m in zip(profile["vol"], profile["margin"]):
           if v > 0 and m > 30: colors.append('#10B981') # Driver
           elif v < 0 and m < 30: colors.append('#EF4444') # Dragger
           else: colors.append('#3B82F6') # Neutral/Steady

       fig_matrix = go.Figure()
       fig_matrix.add_trace(go.Scatter(
           x=profile["vol"], y=profile["margin"],
           mode='markers+text', text=sku_names, textposition="top center",
           marker=dict(size=18, color=colors, line=dict(width=1, color='white'))
       ))
       
       # Grid lines to define quadrants
       fig_matrix.add_hline(y=30, line_dash="dash", line_color="#94A3B8", annotation_text="Margin Target")
       fig_matrix.add_vline(x=0, line_dash="dash", line_color="#94A3B8")
       
       fig_matrix.update_layout(height=400, xaxis_title="Volume Growth (%)", yaxis_title="Gross Margin %",
                                margin=dict(t=30, b=0), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#F8F9FA")
       st.plotly_chart(fig_matrix, use_container_width=True)

       st.markdown("---")
       
       # 4. MARGIN WATERFALL (DYNAMIC)
       col_wf, col_roi = st.columns([2, 1])

       with col_wf:
           st.subheader(f"Margin Waterfall: {sel_retailer}")
           wf_vals = profile["wf"]
           fig_wf = go.Figure(go.Waterfall(
               orientation = "v",
               measure = ["relative", "relative", "relative", "relative", "total"],
               x = ["Gross Sales", "Trade Spend", "COGS", "Supply Chain", "Net Margin"],
               y = wf_vals,
               text = [f"{v}%" if i < 4 else f"Net: {v}%" for i, v in enumerate(wf_vals)],
               decreasing = {"marker":{"color":"#EF4444"}},
               increasing = {"marker":{"color":"#10B981"}},
               totals = {"marker":{"color":"#0E1629"}}
           ))
           fig_wf.update_layout(height=350, margin=dict(t=20, b=20), paper_bgcolor="rgba(0,0,0,0)")
           st.plotly_chart(fig_wf, use_container_width=True)

       with col_roi:
         st.subheader("Trade ROI Calculator")
         with st.container(border=True):
             st.write(f"**Retailer:** {sel_retailer}")
             promo_spend = st.number_input("Est. Promo Spend ($)", value=25000, step=1000)
             incremental_vol = st.number_input("Incremental Volume (Units)", value=12000, step=500)
             unit_margin = st.number_input("Unit Margin ($)", value=3.50)
             
             # Formula: (Incremental Volume * Unit Margin) / Promo Spend
             calc_roi = round((incremental_vol * unit_margin) / promo_spend, 2)
             
             st.markdown("---")
             st.metric("Predicted Trade ROI", f"{calc_roi}x", delta=f"{round(calc_roi - 2.5, 1)}x vs Target")
             if calc_roi >= 2.5:
                 st.success("ROI meets the 2.5x target.")
             else:
                 st.error("ROI is below 2.5x efficiency target.")


# --- MODULE 3: TPO SIMULATOR (UPDATED TO MATCH PDF) ---
# --- MODULE 3: TPO SIMULATOR (FUNCTIONAL & REALISTIC) ---
elif st.session_state.page == 'TPO':
    st.title("📈 TPO Simulator")
    st.markdown("Model promotional scenarios and predict volume lift, revenue, and ROI")
    
    # 1. INPUT PARAMETERS (Top Bar)
    with st.container(border=True):
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1: retailer = st.selectbox("Retailer", ["Walmart", "Target", "Kroger"], index=0)
        with col2: product = st.selectbox("Product", ["Reynolds Wrap 200sqft", "Hefty Ultra Strong"], index=0)
        with col3: disc_type = st.selectbox("Discount Type", ["% Off", "BOGO", "TPR"], index=0)
        with col4: disc_amt = st.number_input("Discount Amount (%)", value=20, step=5)
        with col5: duration = st.number_input("Duration (weeks)", value=2, step=1)
        
        # The trigger for the simulation
        run_sim = st.button("🚀 Run Simulation", type="primary", use_container_width=True)

    # 2. CALCULATION LOGIC (Triggered by Button)
    # Baseline Data from PDF Page 1
    base_vol, base_rev, base_margin = 42000, 168000, 58800
    
    if run_sim or 'sim_results' in st.session_state:
        # Simple elasticity model for realism: Higher discount = Higher Volume Lift, Lower Margin
        lift_factor = (disc_amt / 100) * 1.75  # 20% disc ~ 35% lift
        
        # Scenario 1 (User Input)
        s1_vol = int(base_vol * (1 + lift_factor))
        s1_rev = int(base_rev * (1 + (lift_factor * 0.7))) # Revenue grows slower than volume due to discount
        s1_margin = int(base_margin * (1 - (disc_amt / 100 * 1.2))) # Margin drops as discount increases
        s1_roi = round((s1_rev - base_rev) / (base_rev - s1_margin + 1), 1) + 1.0 # Mock ROI calc

        # Scenario 2 (Aggressive Comparison - Fixed +20% over Scenario 1)
        s2_vol = int(s1_vol * 1.2)
        s2_rev = int(s1_rev * 1.1)
        s2_margin = int(s1_margin * 0.85)
        s2_roi = round(s1_roi * 0.6, 1)

        # 3. KPI CARDS (TOP SECTION)
        st.markdown("### Executive Summary")
        k1, k2, k3 = st.columns(3)
        
        with k1:
            st.markdown("<div style='border-left:5px solid #94A3B8; padding-left:10px;'><b>Baseline</b></div>", unsafe_allow_html=True)
            st.metric("Volume", f"{base_vol:,}")
            st.metric("Net Margin", f"${base_margin:,}")
            st.caption("ROI: 0.0x")

        with k2:
            st.markdown("<div style='border-left:5px solid #3B82F6; padding-left:10px;'><b>Scenario 1 (Current)</b></div>", unsafe_allow_html=True)
            st.metric("Volume", f"{s1_vol:,}", f"{int(lift_factor*100)}% Lift")
            st.metric("Net Margin", f"${s1_margin:,}", f"{int(((s1_margin/base_margin)-1)*100)}%", delta_color="inverse")
            st.markdown(f"<h3 style='color:#10B981; margin:0;'>ROI: {s1_roi}x</h3>", unsafe_allow_html=True)

        with k3:
            st.markdown("<div style='border-left:5px solid #8B5CF6; padding-left:10px;'><b>Scenario 2 (Aggressive)</b></div>", unsafe_allow_html=True)
            st.metric("Volume", f"{s2_vol:,}", "55% Lift")
            st.metric("Net Margin", f"${s2_margin:,}", "-35%", delta_color="inverse")
            st.markdown(f"<h3 style='color:{'#10B981' if s2_roi >= 1 else '#EF4444'}; margin:0;'>ROI: {s2_roi}x</h3>", unsafe_allow_html=True)

        # 4. GRAPHS & RECOMMENDATION (BOTTOM SECTION)
        st.markdown("---")
        g_col, r_col = st.columns([2, 1])

        with g_col:
            st.subheader("Volume vs Revenue Comparison")
            fig = go.Figure()
            fig.add_trace(go.Bar(name='Baseline', x=['Vol', 'Rev'], y=[base_vol, base_rev], marker_color='#94A3B8'))
            fig.add_trace(go.Bar(name='Scenario 1', x=['Vol', 'Rev'], y=[s1_vol, s1_rev], marker_color='#3B82F6'))
            fig.add_trace(go.Bar(name='Scenario 2', x=['Vol', 'Rev'], y=[s2_vol, s2_rev], marker_color='#8B5CF6'))
            fig.update_layout(barmode='group', height=300, margin=dict(t=0,b=0,l=0,r=0), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)

        with r_col:
            st.subheader("Recommendation")
            if s1_roi > s2_roi:
                st.success(f"**Scenario 1** is recommended. It yields a healthier ROI of **{s1_roi}x** while maintaining margin stability.")
            else:
                st.warning(f"**Scenario 2** maximizes volume, but ROI drops to **{s2_roi}x**. Proceed only for market share gains.")
            
            st.info(f"💡 **Insight**: At {retailer}, {disc_amt}% discount is the 'sweet spot' for {product}.")

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
