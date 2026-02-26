import streamlit as st
import streamlit.components.v1 as components
import time

# --- Page Config ---
st.set_page_config(page_title="Warehouse AGV Monitor", layout="wide")

# --- Custom CSS for Large Dropdowns & Status Box ---
st.markdown("""
    <style>
    /* Make Dropdowns larger */
    div[data-testid="stSelectbox"] label p {
        font-size: 20px !important;
        font-weight: bold;
    }
    div[data-testid="stSelectbox"] div[data-baseweb="select"] {
        font-size: 18px !important;
        padding: 5px;
    }
    
    .status-box {
        background-color: #00C853;
        color: white;
        padding: 25px;
        border-radius: 15px;
        font-family: sans-serif;
        margin-top: 30px;
        font-size: 18px;
    }
    /* Master Progress Bar Color (Blue) */
    div[data-testid="stProgress"] > div > div > div > div {
        background-color: #4A90E2;
    }
    </style>
    """, unsafe_allow_html=True)

# --- State Management ---
if 'target_y' not in st.session_state: st.session_state.target_y = 450
if 'active_agv' not in st.session_state: st.session_state.active_agv = None
if 'mission_step' not in st.session_state: st.session_state.mission_step = "idle"

RACK_COORDINATES = {
    "L3": 90, "R3": 90,
    "L2": 220, "R2": 220,
    "L1": 350, "R1": 350
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
    
    if st.button("Start Mission", use_container_width=True):
        st.session_state.target_y = RACK_COORDINATES[rack]
        st.session_state.active_agv = "S" if rack.startswith("L") else "M"
        st.session_state.mission_step = "moving_to_rack"
        st.rerun()

    agv_display = "Slave" if rack.startswith("L") else "Master"
    st.markdown(f"""
    <div class="status-box">
        <strong>Operation Status :</strong><br><br>
        AGV under performance : {agv_display}<br>
        State of Charge : 76%
    </div>
    """, unsafe_allow_html=True)

with col2:
    # Determine positions for the SVG
    # If idle, both are at dock (450). If moving, active one goes to target_y.
    s_pos = st.session_state.target_y if st.session_state.active_agv == "S" else 450
    m_pos = st.session_state.target_y if st.session_state.active_agv == "M" else 450

    # The transition style makes the movement smooth over 2 seconds
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

            <rect x="70" y="70" width="70" height="40" fill="white" stroke="grey" /> <text x="95" y="95" font-family="Arial">L3</text>
            <rect x="360" y="70" width="70" height="40" fill="white" stroke="grey" /> <text x="385" y="95" font-family="Arial">R3</text>
            <rect x="70" y="200" width="70" height="40" fill="white" stroke="grey" /> <text x="95" y="225" font-family="Arial">L2</text>
            <rect x="360" y="200" width="70" height="40" fill="white" stroke="grey" /> <text x="385" y="225" font-family="Arial">R2</text>
            <rect x="70" y="330" width="70" height="40" fill="white" stroke="grey" /> <text x="95" y="355" font-family="Arial">L1</text>
            <rect x="360" y="330" width="70" height="40" fill="white" stroke="grey" /> <text x="385" y="355" font-family="Arial">R1</text>

            <rect x="180" y="{s_pos}" width="40" height="60" rx="5" fill="#FF5252" style="transition: all 2s ease-in-out;" />
            <text x="193" y="{s_pos + 35}" fill="white" font-weight="bold" style="transition: all 2s ease-in-out;">S</text>
            
            <rect x="280" y="{m_pos}" width="40" height="60" rx="5" fill="#4A90E2" style="transition: all 2s ease-in-out;" />
            <text x="293" y="{m_pos + 35}" fill="white" font-weight="bold" style="transition: all 2s ease-in-out;">M</text>
            
            <rect x="180" y="530" width="70" height="60" fill="#FF5252" opacity="0.9" />
            <rect x="250" y="530" width="70" height="60" fill="#4A90E2" opacity="0.9" />
            <text x="145" y="615" font-family="Arial" font-size="12" font-weight="bold">WIRELESS CHARGING DOCK</text>
        </svg>
    </div>
    """
    components.html(svg_html, height=640)

# --- Automatic Return Logic ---
if st.session_state.mission_step == "moving_to_rack":
    time.sleep(5) # Give it 2s to move + 3s to stay
    st.session_state.target_y = 450
    st.session_state.mission_step = "returning"
    st.rerun()

if st.session_state.mission_step == "returning":
    time.sleep(2) # Time for return transition
    st.session_state.active_agv = None
    st.session_state.mission_step = "idle"
    st.rerun()
