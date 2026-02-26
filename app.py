import streamlit as st
import streamlit.components.v1 as components

# --- Page Config ---
st.set_page_config(page_title="Warehouse AGV Monitor", layout="wide")

# --- Custom CSS for Ultra-Large UI ---
st.markdown("""
    <style>
    /* Ultra-Large Dropdowns and Labels */
    .stSelectbox div[data-baseweb="select"] {
        font-size: 24px !important;
        height: 70px !important;
    }
    .stSelectbox label p {
        font-size: 26px !important;
        font-weight: bold !important;
        color: #333;
    }
    
    .status-box {
        background-color: #00C853;
        color: white;
        padding: 30px;
        border-radius: 15px;
        font-family: sans-serif;
        margin-top: 40px;
        font-size: 22px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Progress Bar Customization */
    div[data-testid="stProgress"] > div > div > div > div {
        background-color: #4A90E2;
    }
    </style>
    """, unsafe_allow_html=True)

# --- State Management ---
if 'mission_id' not in st.session_state:
    st.session_state.mission_id = 0

RACK_COORDINATES = {
    "L3": 90, "R3": 90,
    "L2": 220, "R2": 220,
    "L1": 350, "R1": 350
}

# --- UI Layout ---
col1, col2 = st.columns([1, 1.5])

with col1:
    st.write("### Master Charge")
    st.progress(0.28, text="28%")
    st.write("### Slave Charge")
    st.progress(0.76, text="76%")
    st.markdown("---")
    
    rack = st.selectbox("Product Rack", ["L1", "L2", "L3", "R1", "R2", "R3"], index=4)
    product = st.selectbox("Product Name", [
        "Bearing 5 cm", "Bearing 10 cm", "Bearing 15 cm",
        "Gear 5 cm", "Gear 10 cm", "Gear 15 cm",
        "Shaft 5 cm", "Shaft 10 cm", "Shaft 15 cm"
    ], index=1)
    
    if st.button("EXECUTE MISSION", use_container_width=True):
        st.session_state.mission_id += 1 

    agv_display = "Slave (S)" if rack.startswith("L") else "Master (M)"
    st.markdown(f"""
    <div class="status-box">
        <strong>Operation Status</strong><br><br>
        Active Unit: {agv_display}<br>
        Target: {rack}<br>
        Status: {"In Motion" if st.session_state.mission_id > 0 else "Idle"}
    </div>
    """, unsafe_allow_html=True)

with col2:
    active_agv_id = "slave_agv" if rack.startswith("L") else "master_agv"
    target_y_offset = RACK_COORDINATES[rack] - 450

    # Smooth Animation Logic using RequestAnimationFrame for outbound flow clarity
    html_code = f"""
    <div style="display: flex; justify-content: center; background: white; border: 2px solid #eee; border-radius: 20px; padding: 10px;">
        <svg id="warehouse_map" width="500" height="630" viewBox="0 0 500 630" xmlns="http://www.w3.org/2000/svg">
            
            <line x1="60" y1="90" x2="440" y2="90" stroke="#FF5252" stroke-width="2" opacity="0.15" />
            <line x1="60" y1="220" x2="440" y2="220" stroke="#FF5252" stroke-width="2" opacity="0.15" />
            <line x1="60" y1="350" x2="440" y2="350" stroke="#FF5252" stroke-width="2" opacity="0.15" />
            
            <line x1="60" y1="130" x2="440" y2="130" stroke="#4A90E2" stroke-width="2" opacity="0.15" />
            <line x1="60" y1="260" x2="440" y2="260" stroke="#4A90E2" stroke-width="2" opacity="0.15" />
            <line x1="60" y1="390" x2="440" y2="390" stroke="#4A90E2" stroke-width="2" opacity="0.15" />

            <line x1="200" y1="50" x2="200" y2="520" stroke="#FF5252" stroke-width="4" opacity="0.8" /> 
            <line x1="300" y1="50" x2="300" y2="520" stroke="#4A90E2" stroke-width="4" opacity="0.8" />

            <g fill="white" stroke="#999" stroke-width="1">
                <rect x="70" y="70" width="70" height="40" /> <text x="95" y="95" stroke="none" fill="black" font-family="Arial">L3</text>
                <rect x="360" y="70" width="70" height="40" /> <text x="385" y="95" stroke="none" fill="black" font-family="Arial">R3</text>
                <rect x="70" y="200" width="70" height="40" /> <text x="95" y="225" stroke="none" fill="black" font-family="Arial">L2</text>
                <rect x="360" y="200" width="70" height="40" /> <text x="385" y="225" stroke="none" fill="black" font-family="Arial">R2</text>
                <rect x="70" y="330" width="70" height="40" /> <text x="95" y="355" stroke="none" fill="black" font-family="Arial">L1</text>
                <rect x="360" y="330" width="70" height="40" /> <text x="385" y="355" stroke="none" fill="black" font-family="Arial">R1</text>
            </g>

            <g id="slave_agv" style="transition: transform 2.5s ease-in-out;">
                <rect x="180" y="450" width="40" height="60" rx="8" fill="#FF5252" />
                <text x="193" y="488" fill="white" font-weight="bold" font-family="Arial">S</text>
            </g>
            
            <g id="master_agv" style="transition: transform 2.5s ease-in-out;">
                <rect x="280" y="450" width="40" height="60" rx="8" fill="#4A90E2" />
                <text x="293" y="488" fill="white" font-weight="bold" font-family="Arial">M</text>
            </g>
            
            <rect x="180" y="530" width="140" height="70" rx="5" fill="#f8f9fa" stroke="#ccc" />
            <text x="195" y="570" font-family="Arial" font-size="10" font-weight="bold" fill="#666">WIRELESS CHARGING DOCK</text>
        </svg>

        <script>
            const missionId = {st.session_state.mission_id};
            if (missionId > 0) {{
                const agv = document.getElementById("{active_agv_id}");
                
                // Force a reflow to ensure the browser captures the 'starting' position
                window.requestAnimationFrame(() => {{
                    window.requestAnimationFrame(() => {{
                        // 1. Outbound Move (2.5 seconds)
                        agv.style.transform = "translateY({target_y_offset}px)";
                        
                        // 2. Wait 3 seconds + 2.5 seconds (travel time) = 5.5s total before return
                        setTimeout(() => {{
                            agv.style.transform = "translateY(0px)";
                        }}, 5500);
                    }});
                }});
            }}
        </script>
    </div>
    """
    components.html(html_code, height=660)
