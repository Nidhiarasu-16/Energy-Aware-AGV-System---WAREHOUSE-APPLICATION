import streamlit as st
import streamlit.components.v1 as components

# --- Page Config ---
st.set_page_config(page_title="Warehouse AGV Monitor", layout="wide")

# --- Deep CSS Injection for Text & Bars ---
st.markdown("""
    <style>
    /* 1. MEGA DROPDOWNS: Target the Label, the Input, and the List Items */
    .stSelectbox label p {
        font-size: 32px !important;
        font-weight: 800 !important;
        color: #1E1E1E !important;
    }
    div[data-baseweb="select"] > div {
        font-size: 28px !important; /* The text you see inside the box */
        height: 70px !important;
        display: flex;
        align-items: center;
    }
    /* The dropdown list items when you click it */
    ul[role="listbox"] li {
        font-size: 26px !important;
        padding: 15px !important;
    }

    /* 2. CUSTOM ENERGY BARS (Since st.progress is too small) */
    .energy-container {
        width: 100%;
        background-color: #e0e0e0;
        border-radius: 15px;
        margin-bottom: 25px;
        border: 2px solid #ccc;
        position: relative;
        height: 50px;
    }
    .energy-fill {
        height: 100%;
        border-radius: 13px;
        display: flex;
        align-items: center;
        justify-content: flex-end;
        padding-right: 20px;
        color: white;
        font-weight: bold;
        font-size: 22px;
        transition: width 0.5s ease-in-out;
    }
    .energy-label {
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 8px;
        display: block;
    }

    /* 3. STATUS BOX & BUTTON */
    .status-box {
        background-color: #00C853;
        color: white;
        padding: 40px;
        border-radius: 20px;
        margin-top: 40px;
        font-size: 28px;
        font-weight: bold;
        line-height: 1.6;
    }
    button[kind="primary"] {
        height: 90px !important;
        font-size: 30px !important;
        font-weight: bold !important;
        background-color: #FF5252 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- State ---
if 'mission_id' not in st.session_state:
    st.session_state.mission_id = 0

RACK_COORDINATES = {
    "L3": 90, "R3": 90, "L2": 220, "R2": 220, "L1": 350, "R1": 350
}

# --- UI Layout ---
col1, col2 = st.columns([1, 1.3])

with col1:
    # 1. Custom Energy Bars
    st.markdown('<span class="energy-label">Master Energy</span>', unsafe_allow_html=True)
    st.markdown('<div class="energy-container"><div class="energy-fill" style="width: 28%; background-color: #4A90E2;">28%</div></div>', unsafe_allow_html=True)
    
    st.markdown('<span class="energy-label">Slave Energy</span>', unsafe_allow_html=True)
    st.markdown('<div class="energy-container"><div class="energy-fill" style="width: 76%; background-color: #4A90E2;">76%</div></div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 2. Large Dropdowns
    rack = st.selectbox("Product Rack", ["L1", "L2", "L3", "R1", "R2", "R3"], index=4)
    product = st.selectbox("Product Name", [
        "Bearing 5 cm", "Bearing 10 cm", "Bearing 15 cm",
        "Gear 5 cm", "Gear 10 cm", "Gear 15 cm",
        "Shaft 5 cm", "Shaft 10 cm", "Shaft 15 cm"
    ], index=1)
    
    # 3. Action
    if st.button("EXECUTE MISSION", type="primary", use_container_width=True):
        st.session_state.mission_id += 1 

    # 4. Status Box
    agv_display = "Slave (S)" if rack.startswith("L") else "Master (M)"
    st.markdown(f"""
    <div class="status-box">
        SYSTEM STATUS:<br>
        Unit: {agv_display}<br>
        Target: {rack}<br>
        Item: {product}
    </div>
    """, unsafe_allow_html=True)

with col2:
    active_agv_id = "slave_agv" if rack.startswith("L") else "master_agv"
    target_y_offset = RACK_COORDINATES[rack] - 450

    html_code = f"""
    <div style="display: flex; justify-content: center; background: white; border: 3px solid #eee; border-radius: 25px; padding: 15px;">
        <svg id="warehouse_map" width="500" height="630" viewBox="0 0 500 630" xmlns="http://www.w3.org/2000/svg">
            <line x1="60" y1="90" x2="440" y2="90" stroke="#FF5252" stroke-width="2" opacity="0.1" />
            <line x1="60" y1="220" x2="440" y2="220" stroke="#FF5252" stroke-width="2" opacity="0.1" />
            <line x1="60" y1="350" x2="440" y2="350" stroke="#FF5252" stroke-width="2" opacity="0.1" />
            <line x1="60" y1="130" x2="440" y2="130" stroke="#4A90E2" stroke-width="2" opacity="0.1" />
            <line x1="60" y1="260" x2="440" y2="260" stroke="#4A90E2" stroke-width="2" opacity="0.1" />
            <line x1="60" y1="390" x2="440" y2="390" stroke="#4A90E2" stroke-width="2" opacity="0.1" />

            <line x1="200" y1="50" x2="200" y2="520" stroke="#FF5252" stroke-width="5" opacity="0.8" /> 
            <line x1="300" y1="50" x2="300" y2="520" stroke="#4A90E2" stroke-width="5" opacity="0.8" />

            <g fill="white" stroke="#666" stroke-width="1.5">
                <rect x="70" y="70" width="70" height="40" rx="3"/><text x="95" y="95" stroke="none" fill="black" font-family="Arial" font-size="14">L3</text>
                <rect x="360" y="70" width="70" height="40" rx="3"/><text x="385" y="95" stroke="none" fill="black" font-family="Arial" font-size="14">R3</text>
                <rect x="70" y="200" width="70" height="40" rx="3"/><text x="95" y="225" stroke="none" fill="black" font-family="Arial" font-size="14">L2</text>
                <rect x="360" y="200" width="70" height="40" rx="3"/><text x="385" y="225" stroke="none" fill="black" font-family="Arial" font-size="14">R2</text>
                <rect x="70" y="330" width="70" height="40" rx="3"/><text x="95" y="355" stroke="none" fill="black" font-family="Arial" font-size="14">L1</text>
                <rect x="360" y="330" width="70" height="40" rx="3"/><text x="385" y="355" stroke="none" fill="black" font-family="Arial" font-size="14">R1</text>
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
                        setTimeout(() => {{ agv.style.transform = "translateY(0px)"; }}, 5500);
                    }});
                }});
            }}
        </script>
    </div>
    """
    components.html(html_code, height=660)
