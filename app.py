import streamlit as st
import streamlit.components.v1 as components
import time

# --- Page Config ---
st.set_page_config(page_title="Warehouse AGV Monitor", layout="wide")

# --- Custom CSS for Large UI ---
st.markdown("""
    <style>
    /* Large Dropdowns */
    .stSelectbox div[data-baseweb="select"] {
        font-size: 20px !important;
        height: 60px !important;
    }
    .stSelectbox label {
        font-size: 22px !important;
        font-weight: bold !important;
    }
    
    .status-box {
        background-color: #00C853;
        color: white;
        padding: 25px;
        border-radius: 15px;
        font-family: sans-serif;
        margin-top: 30px;
        font-size: 20px;
        font-weight: bold;
    }
    /* Master Progress Bar Color (Blue) */
    div[data-testid="stProgress"] > div > div > div > div {
        background-color: #4A90E2;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Initial State ---
if 'trigger_mission' not in st.session_state:
    st.session_state.trigger_mission = 0

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
        st.session_state.trigger_mission += 1 # Increments to trigger the JS animation

    agv_display = "Slave" if rack.startswith("L") else "Master"
    st.markdown(f"""
    <div class="status-box">
        Operation Status :<br><br>
        AGV under performance : {agv_display}<br>
        State of Charge : 76%
    </div>
    """, unsafe_allow_html=True)

with col2:
    # Logic for JS: which AGV moves and where
    active_agv = "S" if rack.startswith("L") else "M"
    target_y = RACK_COORDINATES[rack]

    # Embedded HTML/JS for smooth, non-resetting animation
    html_code = f"""
    <div style="display: flex; justify-content: center; background: white; border: 1px solid #ccc;">
        <svg id="warehouse" width="500" height="630" viewBox="0 0 500 630" xmlns="http://www.w3.org/2000/svg">
            
            <line x1="70" y1="90" x2="430" y2="90" stroke="#FF5252" stroke-width="2" opacity="0.2" />
            <line x1="70" y1="220" x2="430" y2="220" stroke="#FF5252" stroke-width="2" opacity="0.2" />
            <line x1="70" y1="350" x2="430" y2="350" stroke="#FF5252" stroke-width="2" opacity="0.2" />
            <line x1="70" y1="130" x2="430" y2="130" stroke="#4A90E2" stroke-width="2" opacity="0.2" />
            <line x1="70" y1="260" x2="430" y2="260" stroke="#4A90E2" stroke-width="2" opacity="0.2" />
            <line x1="70" y1="390" x2="430" y2="390" stroke="#4A90E2" stroke-width="2" opacity="0.2" />

            <line x1="200" y1="50" x2="200" y2="520" stroke="#FF5252" stroke-width="4" /> 
            <line x1="300" y1="50" x2="300" y2="520" stroke="#4A90E2" stroke-width="4" />

            <rect x="70" y="70" width="70" height="40" fill="white" stroke="grey" /> <text x="95" y="95" font-family="Arial">L3</text>
            <rect x="360" y="70" width="70" height="40" fill="white" stroke="grey" /> <text x="385" y="95" font-family="Arial">R3</text>
            <rect x="70" y="200" width="70" height="40" fill="white" stroke="grey" /> <text x="95" y="225" font-family="Arial">L2</text>
            <rect x="360" y="200" width="70" height="40" fill="white" stroke="grey" /> <text x="385" y="225" font-family="Arial">R2</text>
            <rect x="70" y="330" width="70" height="40" fill="white" stroke="grey" /> <text x="95" y="355" font-family="Arial">L1</text>
            <rect x="360" y="330" width="70" height="40" fill="white" stroke="grey" /> <text x="385" y="355" font-family="Arial">R1</text>

            <g id="slave_agv" transform="translate(0,0)">
                <rect x="180" y="450" width="40" height="60" rx="5" fill="#FF5252" />
                <text x="193" y="485" fill="white" font-weight="bold">S</text>
            </g>
            
            <g id="master_agv" transform="translate(0,0)">
                <rect x="280" y="450" width="40" height="60" rx="5" fill="#4A90E2" />
                <text x="293" y="485" fill="white" font-weight="bold">M</text>
            </g>
            
            <rect x="180" y="530" width="70" height="60" fill="#FF5252" opacity="0.9" />
            <rect x="250" y="530" width="70" height="60" fill="#4A90E2" opacity="0.9" />
            <text x="145" y="615" font-family="Arial" font-size="12" font-weight="bold">WIRELESS CHARGING DOCK</text>
        </svg>

        <script>
            function animateAGV() {{
                const agv = document.getElementById("{'slave_agv' if active_agv == 'S' else 'master_agv'}");
                const targetY = {target_y - 450}; // Calculate relative offset
                
                // 1. Move to Rack (2 seconds)
                agv.style.transition = "transform 2s ease-in-out";
                agv.style.transform = `translateY(${{targetY}}px)`;
                
                // 2. Stay for 3 seconds, then return
                setTimeout(() => {{
                    agv.style.transform = "translateY(0px)";
                }}, 5000); 
            }}
            
            // Trigger animation if the button was clicked
            if ({st.session_state.trigger_mission} > 0) {{
                animateAGV();
            }}
        </script>
    </div>
    """
    components.html(html_code, height=650)
