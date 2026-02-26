import streamlit as st
import time

# --- Page Config ---
st.set_page_config(page_title="Warehouse AGV Monitor", layout="wide")

# --- Custom CSS for Styling ---
st.markdown("""
    <style>
    .status-box {
        background-color: #00C853;
        color: white;
        padding: 20px;
        border-radius: 15px;
        font-family: sans-serif;
    }
    .stProgress > div > div > div > div {
        background-color: #4A90E2;
    }
    </style>
    """, unsafe_allow_index=True)

# --- Initial State ---
if 'm_pos' not in st.session_state:
    st.session_state.m_pos = 0  # 0 is home, 1 is target
    st.session_state.s_pos = 0
    st.session_state.is_moving = False

# --- UI Layout ---
col1, col2 = st.columns([1, 1.5])

with col1:
    # Charge Indicators
    st.write("### Master")
    st.progress(0.28, text="28%")
    
    st.write("### Slave")
    st.progress(0.76, text="76%")
    
    st.markdown("---")
    
    # Dropdowns
    rack = st.selectbox("Product Rack", ["L1", "L2", "L3", "R1", "R2", "R3"], index=4)
    product = st.selectbox("Product Name", [
        "Bearing 5 cm", "Bearing 10 cm", "Bearing 15 cm",
        "Gear 5 cm", "Gear 10 cm", "Gear 15 cm",
        "Shaft 5 cm", "Shaft 10 cm", "Shaft 15 cm"
    ], index=1)
    
    if st.button("Start Mission") and not st.session_state.is_moving:
        st.session_state.is_moving = True
        # Logic: Racks L use Slave (Red), Racks R use Master (Blue)
        agv_type = "S" if rack.startswith("L") else "M"
        
        # Move forward
        if agv_type == "S": st.session_state.s_pos = 1
        else: st.session_state.m_pos = 1
        st.rerun()

    # Operation Status Box
    st.markdown(f"""
    <div class="status-box">
        <strong>Operation Status :</strong><br><br>
        AGV under performance : {"Slave" if rack.startswith("L") else "Master"}<br>
        State of Charge : 76
    </div>
    """, unsafe_allow_index=True)

with col2:
    # Determine SVG positions based on state
    # Simplified Y-coordinates for "Home" vs "Target"
    m_y = 450 if st.session_state.m_pos == 0 else 250
    s_y = 450 if st.session_state.s_pos == 0 else 250

    # Build the Warehouse Layout SVG
    svg_layout = f"""
    <svg width="500" height="600" viewBox="0 0 500 600" xmlns="http://www.w3.org/2000/svg">
        <rect x="50" y="50" width="400" height="400" fill="none" stroke="black" stroke-width="1"/>
        
        <rect x="70" y="70" width="70" height="40" fill="white" stroke="grey" /> <text x="95" y="95">L3</text>
        <rect x="360" y="70" width="70" height="40" fill="white" stroke="grey" /> <text x="385" y="95">R3</text>
        <rect x="70" y="200" width="70" height="40" fill="white" stroke="grey" /> <text x="95" y="225">L2</text>
        <rect x="360" y="200" width="70" height="40" fill="white" stroke="grey" /> <text x="385" y="225">R2</text>
        <rect x="70" y="330" width="70" height="40" fill="white" stroke="grey" /> <text x="95" y="355">L1</text>
        <rect x="360" y="330" width="70" height="40" fill="white" stroke="grey" /> <text x="385" y="355">R1</text>
        
        <line x1="200" y1="130" x2="200" y2="450" stroke="red" stroke-width="3" />
        <line x1="100" y1="130" x2="300" y2="130" stroke="red" stroke-width="2" opacity="0.5"/>
        <line x1="100" y1="260" x2="300" y2="260" stroke="red" stroke-width="2" opacity="0.5"/>
        
        <line x1="300" y1="130" x2="300" y2="450" stroke="blue" stroke-width="3" />
        <line x1="200" y1="170" x2="400" y2="170" stroke="blue" stroke-width="2" opacity="0.5"/>
        <line x1="200" y1="300" x2="400" y2="300" stroke="blue" stroke-width="2" opacity="0.5"/>

        <rect x="180" y="{s_y}" width="40" height="60" rx="5" fill="#f55" />
        <text x="193" y="{s_y+35}" fill="black" font-weight="bold">S</text>
        
        <rect x="280" y="{m_y}" width="40" height="60" rx="5" fill="#4A90E2" />
        <text x="293" y="{m_y+35}" fill="black" font-weight="bold">M</text>
        
        <rect x="50" y="520" width="200" height="80" fill="#f55" opacity="0.8" />
        <rect x="250" y="520" width="200" height="80" fill="#4A90E2" opacity="0.8" />
        <text x="140" y="580" fill="white" font-size="12">WIRELESS CHARGING DOCK</text>
    </svg>
    """
    st.write(svg_layout, unsafe_allow_index=True)

# --- Animation Handling ---
if st.session_state.is_moving:
    time.sleep(3) # Wait at target
    st.session_state.m_pos = 0
    st.session_state.s_pos = 0
    st.session_state.is_moving = False
    st.rerun()
