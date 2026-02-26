import streamlit as st
import streamlit.components.v1 as components

# --- Page Config ---
st.set_page_config(page_title="AGV Precision Control", layout="wide")

# --- Aesthetic Industrial CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #060d17; }
    .stSelectbox label p { font-size: 26px !important; font-weight: bold !important; color: #cbd5e1 !important; }
    div[data-baseweb="select"] > div { font-size: 22px !important; height: 65px !important; background: #1e293b !important; color: white !important; border: 1px solid #334155 !important; }
    .energy-container { margin-bottom: 30px; }
    .energy-label { font-size: 20px; font-weight: bold; margin-bottom: 5px; display: block; }
    .bar-outline { width: 100%; border: 2px solid #4A90E2; height: 35px; border-radius: 20px; padding: 3px; background: transparent; }
    .bar-fill { height: 100%; border-radius: 15px; transition: width 1s ease-in-out; }
    .percent-text { color: #4A90E2; font-weight: bold; margin-left: 10px; font-size: 18px; }
    button[kind="primary"] { height: 70px !important; font-size: 24px !important; font-weight: bold !important; background: #FF5252 !important; border-radius: 12px !important; }
    .op-status { background: #00C853; color: white; padding: 25px; border-radius: 15px; font-size: 22px; margin-top: 20px; font-family: sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# --- Dynamic Data Logic ---
m_charge = 28
s_charge = 76

# Constraint: Higher charge unit is selected automatically
if s_charge >= m_charge:
    active_unit, active_id, active_color, unit_label = "S", "slave_agv", "#FF5252", "Slave"
    start_x = 200 # Center of Red Vertical Line
else:
    active_unit, active_id, active_color, unit_label = "M", "master_agv", "#4A90E2", "Master"
    start_x = 300 # Center of Blue Vertical Line

if 'execute_nav' not in st.session_state:
    st.session_state.execute_nav = False

# Mapping Racks to YOUR specified line coordinates
# Slave paths: 45, 185, 325 | Master paths: 165, 305
RACK_PATHS = {
    "L3": {"y": 45,  "x": 80},  
    "R3": {"y": 45,  "x": 420}, 
    "L2": {"y": 165, "x": 80},  
    "R2": {"y": 185, "x": 420}, 
    "L1": {"y": 305, "x": 80},  
    "R1": {"y": 325, "x": 420}  
}

col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.markdown(f'''
    <div class="energy-container">
        <span class="energy-label" style="color:#4A90E2;">Master</span>
        <div style="display:flex; align-items:center;">
            <div class="bar-outline"><div class="bar-fill" style="width:28%; background:#4A90E2;"></div></div>
            <span class="percent-text">28%</span>
        </div>
    </div>
    <div class="energy-container">
        <span class="energy-label" style="color:#FF5252;">Slave</span>
        <div style="display:flex; align-items:center;">
            <div class="bar-outline" style="border-color:#FF5252;"><div class="bar-fill" style="width:76%; background:#FF5252;"></div></div>
            <span class="percent-text" style="color:#FF5252;">76%</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    rack_choice = st.selectbox("Product Rack", list(RACK_PATHS.keys()), index=3) 
    product_choice = st.selectbox("Product Name", ["Bearing 5cm","Bearing 10cm","Bearing 15cm", "Gear 5cm","Gear 10cm","Gear 15cm", "Shaft 5cm","Shaft 10cm","Shaft 15cm"])
    
    if st.button("EXECUTE MISSION", type="primary", use_container_width=True):
        st.session_state.execute_nav = True

    st.markdown(f'<div class="op-status"><b>Operation Status :</b><br><br>AGV under performance : {unit_label}<br>State of Charge : {s_charge if active_unit=="S" else m_charge}%</div>', unsafe_allow_html=True)

with col2:
    # Get target from your coordinates
    conf = RACK_PATHS[rack_choice]
    # start_y = 480 (from your code), start_x = 200 or 300
    dist_y = conf['y'] - 480
    dist_x = conf['x'] - start_x
    
    nav_trigger = "true" if st.session_state.execute_nav else "false"

    # YOUR EXACT SVG LAYOUT
    svg_layout = f"""
    <div style="background: white; border-radius: 10px; padding: 10px;">
        <svg width="100%" height="650" viewBox="0 0 500 650">
            <rect x="10" y="10" width="480" height="500" fill="none" stroke="#ccc" />
            
            <line x1="60" y1="165" x2="440" y2="165" stroke="#4A90E2" stroke-width="3" />
            <line x1="60" y1="305" x2="440" y2="305" stroke="#4A90E2" stroke-width="3" />

           
            <line x1="60" y1="185" x2="440" y2="185" stroke="#FF5252" stroke-width="3" />
            <line x1="60" y1="325" x2="440" y2="325" stroke="#FF5252" stroke-width="3" />

            <line x1="200" y1="50" x2="200" y2="510" stroke="#FF5252" stroke-width="3" />
            <line x1="300" y1="50" x2="300" y2="510" stroke="#4A90E2" stroke-width="3" />

            <g fill="white" stroke="grey" font-family="Arial">
                <rect x="50" y="80" width="60" height="40" /><text x="65" y="105" stroke="none" fill="black">L3</text>
                <rect x="390" y="80" width="60" height="40" /><text x="405" y="105" stroke="none" fill="black">R3</text>
                <rect x="50" y="220" width="60" height="40" /><text x="65" y="245" stroke="none" fill="black">L2</text>
                <rect x="390" y="220" width="60" height="40" /><text x="405" y="245" stroke="none" fill="black">R2</text>
                <rect x="50" y="360" width="60" height="40" /><text x="65" y="385" stroke="none" fill="black">L1</text>
                <rect x="390" y="360" width="60" height="40" /><text x="405" y="385" stroke="none" fill="black">R1</text>
            </g>

            <g id="slave_agv" style="transition: transform 1.5s ease-in-out;">
                <rect x="180" y="480" width="40" height="60" rx="5" fill="#FF5252" />
                <text x="193" y="515" fill="white" font-weight="bold">S</text>
            </g>

            <g id="master_agv" style="transition: transform 1.5s ease-in-out;">
                <rect x="280" y="480" width="40" height="60" rx="5" fill="#4A90E2" />
                <text x="293" y="515" fill="white" font-weight="bold">M</text>
            </g>

            <rect x="150" y="550" width="100" height="80" fill="#FF5252" />
            <rect x="250" y="550" width="100" height="80" fill="#4A90E2" />
            <text x="165" y="620" fill="black" font-size="12" font-weight="bold">WIRELESS CHARGING DOCK</text>
        </svg>

        <script>
            if ({nav_trigger}) {{
                const unit = document.getElementById("{active_id}");
                requestAnimationFrame(() => {{
                    requestAnimationFrame(() => {{
                        // Phase 1: Travel UP to your exact line Y
                        unit.style.transform = "translateY({dist_y}px)";
                        
                        // Phase 2: Travel ON your exact line X
                        setTimeout(() => {{
                            unit.style.transform = "translateY({dist_y}px) translateX({dist_x}px)";
                        }}, 1600);
                        
                        // Phase 3: Return to track
                        setTimeout(() => {{
                            unit.style.transform = "translateY({dist_y}px) translateX(0px)";
                        }}, 5000);
                        
                        // Phase 4: Return Home
                        setTimeout(() => {{
                            unit.style.transform = "translateY(0px) translateX(0px)";
                        }}, 6600);
                    }});
                }});
            }}
        </script>
    </div>
    """
    components.html(svg_layout, height=670)

if st.session_state.execute_nav:
    st.session_state.execute_nav = False
