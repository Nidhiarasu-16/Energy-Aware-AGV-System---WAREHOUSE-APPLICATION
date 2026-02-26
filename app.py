import streamlit as st
import streamlit.components.v1 as components
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
    /* Set progress bar colors */
    div[data-testid="stProgress"] > div > div > div > div {
        background-color: #4A90E2;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Initial State Management ---
if 'm_y' not in st.session_state:
    st.session_state.m_y = 450  
if 's_y' not in st.session_state:
    st.session_state.s_y = 450  
if 'is_moving' not in st.session_state:
    st.session_state.is_moving = False

RACK_COORDINATES = {
    "L1": 330, "R1": 330,
    "L2": 200, "R2": 200,
    "L3": 70,  "R3": 70
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
    
    if st.button("Start Mission") and not st.session_state.is_moving:
        st.session_state.is_moving = True
        target_y = RACK_COORDINATES[rack]
        
        if rack.startswith("L"):
            st.session_state.s_y = target_y
        else:
            st.session_state.m_y = target_y
        st.rerun()

    agv_name = "Slave" if rack.startswith("L") else "Master"
    st.markdown(f"""
    <div class="status-box">
        <strong>Operation Status :</strong><br><br>
        AGV under performance : {agv_name}<br>
        State of Charge : 76
    </div>
    """, unsafe_allow_html=True)

with col2:
    # We use a component to ensure the SVG is rendered as HTML, not text
    svg_html = f"""
    <div style="display: flex; justify-content: center;">
        <svg width="500" height="600" viewBox="0 0 500 600" xmlns="http://www.w3.org/2000/svg" style="background: white; border: 1px solid #ccc;">
            <rect x="10" y="10" width="480" height="490" fill="none" stroke="#eee" stroke-width="1"/>
            
            <rect x="70" y="70" width="70" height="40" fill="#eee" stroke="grey" /> <text x="95" y="95" font-family="Arial">L3</text>
            <rect x="360" y="70" width="70" height="40" fill="#eee" stroke="grey" /> <text x="385" y="95" font-family="Arial">R3</text>
            <rect x="70" y="200" width="70" height="40" fill="#eee" stroke="grey" /> <text x="95" y="225" font-family="Arial">L2</text>
            <rect x="360" y="200" width="70" height="40" fill="#eee" stroke="grey" /> <text x="385" y="225" font-family="Arial">R2</text>
            <rect x="70" y="330" width="70" height="40" fill="#eee" stroke="grey" /> <text x="95" y="355" font-family="Arial">L1</text>
            <rect x="360" y="330" width="70" height="40" fill="#eee" stroke="grey" /> <text x="385" y="355" font-family="Arial">R1</text>
            
            <line x1="200" y1="50" x2="200" y2="500" stroke="#FF5252" stroke-width="4" />
            <line x1="300" y1="50" x2="300" y2="500" stroke="#4A90E2" stroke-width="4" />

            <rect x="180" y="{st.session_state.s_y}" width="40" height="60" rx="5" fill="#FF5252" />
            <text x="193" y="{st.session_state.s_y + 35}" fill="white" font-weight="bold" font-family="Arial">S</text>
            
            <rect x="280" y="{st.session_state.m_y}" width="40" height="60" rx="5" fill="#4A90E2" />
            <text x="293" y="{st.session_state.m_y + 35}" fill="white" font-weight="bold" font-family="Arial">M</text>
            
            <rect x="180" y="520" width="70" height="60" fill="#FF5252" />
            <rect x="250" y="520" width="70" height="60" fill="#4A90E2" />
            <text x="140" y="595" font-family="Arial" font-size="12" font-weight="bold">WIRELESS CHARGING DOCK</text>
        </svg>
    </div>
    """
    components.html(svg_html, height=620)

# --- Animation Logic ---
if st.session_state.is_moving:
    time.sleep(3)
    st.session_state.m_y = 450
    st.session_state.s_y = 450
    st.session_state.is_moving = False
    st.rerun()
