import streamlit as st
import streamlit.components.v1 as components
import time

# --- Page Config ---
st.set_page_config(page_title="Warehouse AGV Monitor", layout="wide")

# --- Custom CSS ---
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
    div[data-testid="stProgress"] > div > div > div > div {
        background-color: #4A90E2;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Initial State ---
# Starting Y is 450 (at the dock)
if 'm_y' not in st.session_state:
    st.session_state.m_y = 450  
if 's_y' not in st.session_state:
    st.session_state.s_y = 450  
if 'is_moving' not in st.session_state:
    st.session_state.is_moving = False

# Mapping Rack names to specific Y-coordinates
RACK_COORDINATES = {
    "L3": 70,  "R3": 70,
    "L2": 200, "R2": 200,
    "L1": 330, "R1": 330
}

# --- UI Layout ---
col1, col2 = st.columns([1, 1.5])

with col1:
    st.write("### Master")
    st.progress(0.28, text="28%")
    st.write("### Slave")
    st.progress(0.76, text="76%")
    st.markdown("---")
    
    rack = st.selectbox("Product Rack", ["L1", "L2", "L3", "R1", "R2", "R3"], index=4)
    product = st.selectbox("Product Name", [
        "Bearing 5 cm", "Bearing 10 cm", "Bearing 15 cm",
        "Gear 5 cm", "Gear 10 cm", "Gear 15 cm",
        "Shaft 5 cm", "Shaft 10 cm", "Shaft 15 cm"
    ], index=1)
    
    start_btn = st.button("Start Mission")

    agv_name = "Slave" if rack.startswith("L") else "Master"
    st.markdown(f"""
    <div class="status-box">
        <strong>Operation Status :</strong><br><br>
        AGV under performance : {agv_name}<br>
        State of Charge : 76
    </div>
    """, unsafe_allow_html=True)

with col2:
    # Build the SVG Warehouse Layout
    svg_html = f"""
    <div style="display: flex; justify-content: center;">
        <svg width="500" height="600" viewBox="0 0 500 600" xmlns="http://www.w3.org/2000/svg" style="background: white; border: 1px solid #ccc;">
            <line x1="70" y1="90" x2="430" y2="90" stroke="#f0f0f0" stroke-width="2" />
            <line x1="70" y1="220" x2="430" y2="220" stroke="#f0f0f0" stroke-width="2" />
            <line x1="70" y1="350" x2="430" y2="350" stroke="#f0f0f0" stroke-width="2" />

            <line x1="200" y1="50" x2="200" y2="500" stroke="#FF5252" stroke-width="4" opacity="0.6" />
            <line x1="300" y1="50" x2="300" y2="500" stroke="#4A90E2" stroke-width="4" opacity="0.6" />

            <rect x="70" y="70" width="70" height="40" fill="white" stroke="grey" /> <text x="95" y="95" font-family="Arial" font-size="12">L3</text>
            <rect x="360" y="70" width="70" height="40" fill="white" stroke="grey" /> <text x="385" y="95" font-family="Arial" font-size="12">R3</text>
            <rect x="70" y="200" width="70" height="40" fill="white" stroke="grey" /> <text x="95" y="225" font-family="Arial" font-size="12">L2</text>
            <rect x="360" y="200" width="70" height="40" fill="white" stroke="grey" /> <text x="385" y="225" font-family="Arial" font-size="12">R2</text>
            <rect x="70" y="330" width="70" height="40" fill="white" stroke="grey" /> <text x="95" y="355" font-family="Arial" font-size="12">L1</text>
            <rect x="360" y="330" width="70" height="40" fill="white" stroke="grey" /> <text x="385" y="355" font-family="Arial" font-size="12">R1</text>

            <rect x="180" y="{st.session_state.s_y}" width="40" height="60" rx="5" fill="#FF5252" />
            <text x="193" y="{st.session_state.s_y + 35}" fill="white" font-weight="bold" font-family="Arial">S</text>
            
            <rect x="280" y="{st.session_state.m_y}" width="40" height="60" rx="5" fill="#4A90E2" />
            <text x="293" y="{st.session_state.m_y + 35}" fill="white" font-weight="bold" font-family="Arial">M</text>
            
            <rect x="180" y="520" width="70" height="60" fill="#FF5252" opacity="0.8" />
            <rect x="250" y="520" width="70" height="60" fill="#4A90E2" opacity="0.8" />
            <text x="145" y="600" font-family="Arial" font-size="12" font-weight="bold">WIRELESS CHARGING DOCK</text>
        </svg>
    </div>
    """
    components.html(svg_html, height=620)

# --- Motion Logic ---
if start_btn and not st.session_state.is_moving:
    st.session_state.is_moving = True
    target_y = RACK_COORDINATES[rack]
    is_slave = rack.startswith("L")
    
    # 1. MOVE TO RACK
    current_y = 450
    while current_y > target_y:
        current_y -= 10  # Speed control
        if is_slave: st.session_state.s_y = current_y
        else: st.session_state.m_y = current_y
        time.sleep(0.05) # "Medium" speed pause
        st.rerun()

    # 2. STAY FOR 3 SECONDS
    time.sleep(3)

    # 3. RETURN TO DOCK
    while current_y < 450:
        current_y += 10
        if is_slave: st.session_state.s_y = current_y
        else: st.session_state.m_y = current_y
        time.sleep(0.05)
        st.rerun()

    st.session_state.is_moving = False
    st.rerun()
