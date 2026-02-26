import streamlit as st
import streamlit.components.v1 as components

# --- Page Config ---
st.set_page_config(page_title="Warehouse AGV Monitor", layout="wide")

# --- Custom CSS for Ultra-Large UI & Energy Bars ---
st.markdown("""
    <style>
    /* Ultra-Large Dropdowns */
    .stSelectbox div[data-baseweb="select"] {
        font-size: 28px !important;
        height: 80px !important;
        border: 2px solid #4A90E2 !important;
    }
    .stSelectbox label p {
        font-size: 30px !important;
        font-weight: bold !important;
        color: #1E1E1E;
        margin-bottom: 10px;
    }
    
    /* Custom Large Energy Bars (Progress Bars) */
    div[data-testid="stProgress"] {
        height: 40px !important;
    }
    div[data-testid="stProgress"] > div > div {
        height: 40px !important;
    }
    /* Text above progress bars */
    div[data-testid="stWidgetLabel"] p {
        font-size: 24px !important;
        font-weight: bold !important;
    }

    .status-box {
        background-color: #00C853;
        color: white;
        padding: 40px;
        border-radius: 20px;
        font-family: sans-serif;
        margin-top: 50px;
        font-size: 26px;
        font-weight: bold;
        box-shadow: 0 10px 20px rgba(0,0,0,0.15);
    }
    
    /* Execution Button */
    button[kind="primary"] {
        height: 80px !important;
        font-size: 25px !important;
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
col1, col2 = st.columns([1, 1.3])

with col1:
    # 1. Supersized Energy Bars
    st.write("## Energy Levels")
    st.progress(0.28, text="MASTER AGV: 28%")
    st.write("") # Spacing
    st.progress(0.76, text="SLAVE AGV: 76%")
    
    st.markdown("<br><hr><br>", unsafe_allow_html=True)
    
    # 2. Large Dropdowns
    rack = st.selectbox("Product Rack", ["L1", "L2", "L3", "R1", "R2", "R3"], index=4)
    product = st.selectbox("Product Name", [
        "Bearing 5 cm", "Bearing 10 cm", "Bearing 15 cm",
        "Gear 5 cm", "Gear 10 cm", "Gear 15 cm",
        "Shaft 5 cm", "Shaft 10 cm", "Shaft 15 cm"
    ], index=1)
    
    # 3. Action Button
    if st.button("EXECUTE MISSION", type="primary", use_container_width=True):
        st.session_state.mission_id += 1 

    # 4. Large Status Box
    agv_display = "Slave (S)" if rack.startswith("L") else "Master (M)"
    st.markdown(f"""
    <div class="status-box">
        OPERATIONAL STATUS<br>
        -------------------------<br>
        AGV: {agv_display}<br>
        Target: {rack}<br>
        Item: {product}
    </div>
    """, unsafe_allow_html=True)

with col2:
    active_agv_id = "slave_agv" if rack.startswith("L") else "master_agv"
    target_y_offset = RACK_COORDINATES[rack] - 450

    html_code = f"""
    <div style="display: flex; justify-content: center; background: white; border: 3px solid #f0f2f6; border-radius: 25px; padding: 15px;">
        <svg id="warehouse_map" width="500" height="630" viewBox="0 0 500 630" xmlns="http://www.w3.org/2000/svg">
            
            <line x1="60" y1="90" x2="440" y2="90" stroke="#FF5252" stroke-width="2" opacity="0.1" />
            <line x1="60" y1="220" x2="440" y2="220" stroke="#FF5252" stroke-width="2" opacity="0.1" />
            <line x1="60" y1="350" x2="440" y2="350" stroke="#FF5252" stroke-width="2" opacity="0.1" />
            
            <line x1="60" y1="130" x2="440" y2="130" stroke="#4A90E2" stroke-width="2" opacity="0.1" />
            <line x1="60" y1="260" x2="440" y2="260" stroke="#4A90E2" stroke-width="2" opacity="0.1" />
            <line x1="60" y1="390" x2="440" y2="390" stroke="#4A90E2" stroke-width="2" opacity="0.1" />

            <line x1="200" y1="50" x2="200" y2="520" stroke="#FF5252" stroke-width="5" opacity="0.9" /> 
            <line x1="300" y1="50" x2="300" y2="520" stroke="#4A90E2" stroke-width="5" opacity="0.9" />

            <g fill="white" stroke="#666" stroke-width="1.5">
                <rect x="70" y="70" width="70" height="40" rx="3"/> <text x="95" y="95" stroke="none" fill="black" font-family="Arial" font-size="14">L3</text>
                <rect x="360" y="70" width="70" height="40" rx="3"/> <text x="385" y="95" stroke="none" fill="black" font-family="Arial" font-size="14">R3</text>
                <rect x="70" y="200" width="70" height="40" rx="3"/> <text x="95" y="225" stroke="none" fill="black" font-family="Arial" font-size="14">L2</text>
                <rect x="360" y="200" width="70" height="40" rx="3"/> <text x="385" y="225" stroke="none" fill="black" font-family="Arial" font-size="14">R2</text>
                <rect x="70" y="330" width="70" height="40" rx="3"/> <text x="95" y="355" stroke="none" fill="black" font-family="Arial" font-size="14">L1</text>
                <rect x="360" y="330" width="70" height="40" rx="3"/> <text x="385" y="355" stroke="none" fill="black" font-family="Arial" font-size="14">R1</text>
            </g>

            <g id="slave_agv" style="transition: transform 2.5s ease-in-out;">
                <rect x="175" y="445" width="50" height="70" rx="10" fill="#FF5252" />
                <text x="193" y="488" fill="white" font-weight="bold" font-family="Arial" font-size="18">S</text>
            </g>
            
            <g id="master_agv" style="transition: transform 2.5s ease-in-out;">
                <rect x="275" y="445" width="50" height="70" rx="10" fill="#4A90E2" />
                <text x="293" y="488" fill="white" font-weight="bold" font-family="Arial" font-size="18">M</text>
            </g>
            
            <rect x="175" y="530" width="150" height="80" rx="10" fill="#f8f9fa" stroke="#ccc" />
            <text x="182" y="575" font-family="Arial" font-size="12" font-weight="bold" fill="#444">CHARGING STATION</text>
        </svg>

        <script>
            const mId = {st.session_state.mission_id};
            if (mId > 0) {{
                const agv = document.getElementById("{active_agv_id}");
                window.requestAnimationFrame(() => {{
                    window.requestAnimationFrame(() => {{
                        agv.style.transform = "translateY({target_y_offset}px)";
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
