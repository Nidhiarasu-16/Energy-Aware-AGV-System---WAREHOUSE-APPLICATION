import streamlit as st
import streamlit.components.v1 as components
import time

st.set_page_config(page_title="Warehouse AGV Monitor", layout="wide")

# --- Persistent State ---
if 's_y' not in st.session_state: st.session_state.s_y = 450
if 'm_y' not in st.session_state: st.session_state.m_y = 450
if 'mission_active' not in st.session_state: st.session_state.mission_active = False

RACK_Y = {"L3": 90, "R3": 90, "L2": 220, "R2": 220, "L1": 350, "R1": 350}

# --- Layout ---
col1, col2 = st.columns([1, 1.5])

with col1:
    st.title("Control Panel")
    rack_choice = st.selectbox("Select Target Rack", ["L1", "L2", "L3", "R1", "R2", "R3"], index=0)
    start_btn = st.button("Start Mission")

# --- The Animated Map (Fragment) ---
@st.fragment
def warehouse_map():
    # This renders the SVG based on current session_state
    svg_html = f"""
    <div style="display: flex; justify-content: center; background: white; padding: 10px; border-radius: 10px;">
        <svg width="500" height="600" viewBox="0 0 500 600" xmlns="http://www.w3.org/2000/svg">
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
            
            <rect x="180" y="525" width="140" height="60" fill="#eee" rx="5" />
            <text x="185" y="560" font-family="Arial" font-size="10" font-weight="bold">CHARGING DOCK</text>
        </svg>
    </div>
    """
    components.html(svg_html, height=620)

with col2:
    warehouse_map()

# --- Motion Animation Trigger ---
if start_btn and not st.session_state.mission_active:
    st.session_state.mission_active = True
    target_y = RACK_Y[rack_choice]
    is_slave = rack_choice.startswith("L")
    
    # 1. MOVE UP
    while (st.session_state.s_y if is_slave else st.session_state.m_y) > target_y:
        if is_slave: st.session_state.s_y -= 5
        else: st.session_state.m_y -= 5
        st.rerun() # Refresh the UI for the next step
        time.sleep(0.01)

    # 2. LOAD PRODUCT
    time.sleep(2)

    # 3. MOVE DOWN
    while (st.session_state.s_y if is_slave else st.session_state.m_y) < 450:
        if is_slave: st.session_state.s_y += 5
        else: st.session_state.m_y += 5
        st.rerun()
        time.sleep(0.01)

    st.session_state.mission_active = False
    st.rerun()
