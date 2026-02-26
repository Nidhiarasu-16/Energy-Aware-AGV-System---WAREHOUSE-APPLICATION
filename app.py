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
        margin-top: 20px;
    }
    /* Master Progress Bar Color (Blue) */
    div[data-testid="stProgress"] > div > div > div > div {
        background-color: #4A90E2;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Initial State Management ---
if 'm_y' not in st.session_state:
    st.session_state.m_y = 450  # Starting Y position for Master (Dock)
if 's_y' not in st.session_state:
    st.session_state.s_y = 450  # Starting Y position for Slave (Dock)
if 'is_moving' not in st.session_state:
    st.session_state.is_moving = False

# Mapping Rack names to specific Y-coordinates on the SVG map
RACK_COORDINATES = {
    "L1": 330, "R1": 330,
    "L2": 200, "R2": 200,
    "L3": 70,  "R3": 70
}

# --- UI Layout ---
col1, col2 = st.columns([1, 1.5])

with col1:
    # Charge Indicators (Predefined values as requested)
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
    
    # Mission Button
    if st.button("Start Mission") and not st.session_state.is_moving:
        st.session_state.is_moving = True
        target_y = RACK_COORDINATES[rack]
        
        # Logic: Racks starting with L use Slave, Racks starting with R use Master
        if rack.startswith("L"):
            st.session_state.s_y = target_y
        else:
            st.session_state.m_y = target_y
        st.rerun()

    # Operation Status Box
    agv_name = "Slave" if rack.startswith("L") else "Master"
    st.markdown(f"""
    <div class="status-box">
        <strong>Operation Status :</strong><br><br>
        AGV under performance : {agv_name}<br>
        State of Charge : 76
    </div>
    """, unsafe_allow_html=True)

with col2:
    # Build the Warehouse Layout SVG dynamically based on session state positions
    svg_layout = f"""
    <svg width="500" height="600" viewBox="0 0 500 600" xmlns="http://www.w3.org/2000/svg">
        <rect x="50" y="20" width="400" height="480" fill="none" stroke="#333" stroke-width="1"/>
        
        <rect x="70" y="70" width="70" height="40" fill="white" stroke="grey" /> <text x="95" y="95" font-family="sans-serif">L3</text>
        <rect x="360" y="70" width="70" height="40" fill="white" stroke="grey" /> <text x="385" y="95" font-family="sans-serif">R3</text>
        <rect x="70" y="200" width="70" height="40" fill="white" stroke="grey" /> <text x="95" y="225" font-family="sans-serif">L2</text>
        <rect x="360" y="200" width="70" height="40" fill="white" stroke="grey" /> <text x="385" y="225" font-family="sans-serif">R2</text>
        <rect x="70" y="330" width="70" height="40" fill="white" stroke="grey" /> <text x="95" y="355" font-family="sans-serif">L1</text>
        <rect x="360" y="330" width="70" height="40" fill="white" stroke="grey" /> <text x="385" y="355" font-family="sans-serif">R1</text>
        
        <line x1="200" y1="70" x2="200" y2="500" stroke="red" stroke-width="3" /> <line x1="300" y1="70" x2="300" y2="500" stroke="blue" stroke-width="3" /> <line x1="140" y1="135" x2="360" y2="135" stroke="#ccc" stroke-dasharray="5,5" />
        <line x1="140" y1="265" x2="360" y2="265" stroke="#ccc" stroke-dasharray="5,5" />

        <rect x="180" y="{st.session_state.s_y}" width="40" height="60" rx="5" fill="#FF5252" />
        <text x="193" y="{st.session_state.s_y + 35}" fill="white" font-weight="bold" font-family="sans-serif">S</text>
        
        <rect x="280" y="{st.session_state.m_y}" width="40" height="60" rx="5" fill="#4A90E2" />
        <text x="293" y="{st.session_state.m_y + 35}" fill="white" font-weight="bold" font-family="sans-serif">M</text>
        
        <rect x="180" y="520" width="140" height="60" fill="#f0f0f0" stroke="#333" />
        <rect x="180" y="520" width="70" height="60" fill="#FF5252" opacity="0.7" />
        <rect x="250" y="520" width="70" height="60" fill="#4A90E2" opacity="0.7" />
        <text x="185" y="600" fill="black" font-size="10" font-family="sans-serif" font-weight="bold">WIRELESS CHARGING DOCK</text>
    </svg>
    """
    st.write(svg_layout, unsafe_allow_html=True)

# --- Animation/Return Logic ---
if st.session_state.is_moving:
    # Simulation: Wait at the rack for 3 seconds
    time.sleep(3)
    # Return to initial position (Dock at Y=450)
    st.session_state.m_y = 450
    st.session_state.s_y = 450
    st.session_state.is_moving = False
    st.rerun()
