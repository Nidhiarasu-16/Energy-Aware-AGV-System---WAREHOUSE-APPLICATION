import streamlit as st
import streamlit.components.v1 as components
import time

# --- Page Config ---
st.set_page_config(page_title="Warehouse AGV Monitor", layout="wide")

# --- Custom CSS for Layout & Colors ---
st.markdown("""
    <style>
    .status-box {
        background-color: #00C853;
        color: white;
        padding: 20px;
        border-radius: 15px;
        font-family: sans-serif;
        margin-top: 20px;
    }
    /* Set progress bar colors to Blue (Master) */
    div[data-testid="stProgress"] > div > div > div > div {
        background-color: #4A90E2;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Initial State Management ---
if 'm_y' not in st.session_state: st.session_state.m_y = 450  
if 's_y' not in st.session_state: st.session_state.s_y = 450  
if 'is_moving' not in st.session_state: st.session_state.is_moving = False

# Mapping Rack names to specific Y-coordinates
RACK_COORDINATES = {
    "L3": 90, "R3": 90,
    "L2": 220, "R2": 220,
    "L1": 350, "R1": 350
}

# --- UI Layout ---
col1, col2 = st.columns([1, 1.5])

with col1:
    # 1. Charge Indicators
    st.write("### Master")
    st.progress(0.28, text="28%")
    st.write("### Slave")
    st.progress(0.76, text="76%")
    st.markdown("---")
    
    # 2. Dropdowns
    rack = st.selectbox("Product Rack", ["L1", "L2", "L3", "R1", "R2", "R3"], index=4)
    product = st.selectbox("Product Name", [
        "Bearing 5 cm", "Bearing 10 cm", "Bearing 15 cm",
        "Gear 5 cm", "Gear 10 cm", "Gear 15 cm",
        "Shaft 5 cm", "Shaft 10 cm", "Shaft 15 cm"
    ], index=1)
    
    # 3. Mission Button
    start_btn = st.button("Start Mission")

    # 4. Operation Status Box
    agv_display_name = "Slave" if rack.startswith("L") else "Master"
    st.markdown(f"""
    <div class="status-box">
        <strong>Operation Status :</strong><br><br>
        AGV under performance : {agv_display_name}<br>
        State of Charge : 76
    </div>
    """, unsafe_allow_html=True)

with col2:
    # SVG Layout with full-width paths and proper layering
    svg_html = f"""
    <div style="display: flex; justify-content: center;">
        <svg width="500" height="630" viewBox="0 0 500 630" xmlns="http://www.w3.org/2000/svg" style="background: white; border: 1px solid #ccc;">
            
            <line x1="70" y1="90" x2="430" y2="90" stroke="#FF5252" stroke-width="2" opacity="0.3" />
            <line x1="70" y1="220" x2="430" y2="220" stroke="#FF5252" stroke-width="2" opacity="0.3" />
            <line x1="70" y1="350" x2="430" y2="350" stroke="#FF5252" stroke-width="2" opacity="0.3" />
            
            <line x1="70" y1="130" x2="430" y2="130" stroke="#4A90E2" stroke-width="2" opacity="0.3" />
            <line x1="70" y1="260" x2="430" y2="260" stroke="#4A90E2" stroke-width="2" opacity="0.3" />
            <line x1="70" y1="390" x2="430" y2="390" stroke="#4A90E2" stroke-width="2" opacity="0.3" />

            <line x1="200" y1="50" x2="200" y2="520" stroke="#FF5252" stroke-width="4" /> 
            <line x1="300" y1="50" x2="300" y2="520" stroke="#4A90E2" stroke-width="4" />

            <rect x="70" y="70" width="70" height="40" fill="white" stroke="grey" /> <text x="95" y="95" font-family="Arial" font-size="12">L3</text>
            <rect x="360" y="70" width="70" height="40" fill="white" stroke="grey" /> <text x="385" y="95" font-family="Arial" font-size="12">R3</text>
            <rect x="70" y="200" width="70" height="40" fill="white" stroke="grey" /> <text x="95" y="225" font-family="Arial" font-size="12">L2</text>
            <rect x="360" y="200" width="70" height="40" fill="white" stroke="grey" /> <text x="385" y="225" font-family="Arial" font-size="12">R2</text>
            <rect x="70" y="330" width="70" height="40" fill="white" stroke="grey" /> <text x="95" y="355" font-family="Arial" font-size="12">L1</text>
            <rect x="360" y="330" width="70" height="40" fill="white" stroke="grey" /> <text x="385" y="355" font-family="Arial" font-size="12">R1</text>

            <rect x="180" y="{st.session_state.s_y}" width="40" height="60" rx="5" fill="#FF5252" />
            <text x="193" y="{st.session_state.s_y + 35}" fill="white" font-weight="bold">S</text>
            
            <rect x="280" y="{st.session_state.m_y}" width="40" height="60" rx="5" fill="#4A90E2" />
            <text x="293" y="{st.session_state.m_y + 35}" fill="white" font-weight="bold">M</text>
            
            <rect x="180" y="530" width="70" height="60" fill="#FF5252" opacity="0.9" />
            <rect x="250" y="530" width="70" height="60" fill="#4A90E2" opacity="0.9" />
            <text x="145" y="615" font-family="Arial" font-size="12" font-weight="bold">WIRELESS CHARGING DOCK</text>
        </svg>
    </div>
    """
    components.html(svg_html, height=640)

# --- Animation Loop ---
if start_btn and not st.session_state.is_moving:
    st.session_state.is_moving = True
    target_y = RACK_COORDINATES[rack]
    is_slave = rack.startswith("L")
    
    # Step 1: Move UP
    while (st.session_state.s_y if is_slave else st.session_state.m_y) > target_y:
        if is_slave: st.session_state.s_y -= 10
        else: st.session_state.m_y -= 10
        time.sleep(0.05)
        st.rerun()

    # Step 2: Hold for 3 seconds
    time.sleep(3)

    # Step 3: Move DOWN
    while (st.session_state.s_y if is_slave else st.session_state.m_y) < 450:
        if is_slave: st.session_state.s_y += 10
        else: st.session_state.m_y += 10
        time.sleep(0.05)
        st.rerun()

    st.session_state.is_moving = False
    st.rerun()
    
