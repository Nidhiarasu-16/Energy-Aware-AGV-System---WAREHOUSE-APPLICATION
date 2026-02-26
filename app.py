import streamlit as st
import streamlit.components.v1 as components

# --- Page Config ---
st.set_page_config(page_title="AGV Intelligent Control", layout="wide")

# --- Aesthetic Glassmorphism CSS ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #060d17 0%, #0f172a 100%); }
    
    .control-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(15px);
        border-radius: 24px;
        padding: 30px;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }

    .energy-header { color: #94a3b8; font-size: 13px; text-transform: uppercase; letter-spacing: 1.2px; margin-bottom: 5px; }
    .energy-bar-bg { width: 100%; background: rgba(255,255,255,0.05); height: 10px; border-radius: 5px; margin-bottom: 20px; }
    .energy-bar-fill { height: 100%; border-radius: 5px; transition: width 1s ease; }

    .stSelectbox label p { color: #cbd5e1 !important; font-size: 16px !important; }
    div[data-baseweb="select"] { background-color: rgba(255,255,255,0.02) !important; border: 1px solid rgba(255,255,255,0.1) !important; color: white !important; }

    button[kind="primary"] {
        background: linear-gradient(90deg, #38bdf8, #818cf8) !important;
        border: none !important; height: 55px !important; border-radius: 12px !important;
        font-weight: bold !important; font-size: 18px !important;
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.2) !important;
    }

    .status-alert {
        padding: 15px; border-radius: 12px; border-left: 4px solid #38bdf8;
        background: rgba(56, 189, 248, 0.05); color: white; margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Logic: Automated Unit Selection ---
master_charge = 28
slave_charge = 76

# The logic: Identify which unit has higher energy
if master_charge >= slave_charge:
    selected_unit = "M"
    active_color = "#38bdf8"
    active_name = "Master Unit"
    current_charge = master_charge
else:
    selected_unit = "S"
    active_color = "#fb7185"
    active_name = "Slave Unit"
    current_charge = slave_charge

# --- State ---
if 'mission_trigger' not in st.session_state:
    st.session_state.mission_trigger = False

# Path coordinates (Aisle Y, Final X)
RACK_PATHS = {
    "L3": {"y": 90, "x": 110}, "R3": {"y": 90, "x": 395},
    "L2": {"y": 220, "x": 110}, "R2": {"y": 220, "x": 395},
    "L1": {"y": 350, "x": 110}, "R1": {"y": 350, "x": 395}
}

col1, col2 = st.columns([1, 1.4], gap="large")

with col1:
    st.markdown('<h2 style="color:white;">Mission <span style="color:#38bdf8;">Plan</span></h2>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="control-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="energy-header">Master Energy: {master_charge}%</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="energy-bar-bg"><div class="energy-bar-fill" style="width: {master_charge}%; background: #38bdf8;"></div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="energy-header">Slave Energy: {slave_charge}%</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="energy-bar-bg"><div class="energy-bar-fill" style="width: {slave_charge}%; background: #fb7185;"></div></div>', unsafe_allow_html=True)
        
        rack_choice = st.selectbox("Destination Rack", list(RACK_PATHS.keys()), index=1)
        st.selectbox("Item Details", ["Bearing 10cm", "Gear 15cm", "Shaft 5cm"])
        
        if st.button("DISPATCH AGV", type="primary", use_container_width=True):
            st.session_state.mission_trigger = True
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(f"""<div class="status-alert">
        <b>Intelligence System:</b> {active_name} selected for mission (Higher Charge: {current_charge}%)
    </div>""", unsafe_allow_html=True)

with col2:
    # Get target coordinates
    path = RACK_PATHS[rack_choice]
    # Calculate offsets relative to starting positions
    # S starts at x:200, y:450 | M starts at x:300, y:450
    start_x = 200 if selected_unit == "S" else 300
    target_dx = path['x'] - start_x
    target_dy = path['y'] - 450
    
    svg_id = "slave_agv" if selected_unit == "S" else "master_agv"

    html_map = f"""
    <div style="background: rgba(255,255,255,0.02); border-radius: 30px; padding: 20px; border: 1px solid rgba(255,255,255,0.05);">
        <svg width="100%" height="650" viewBox="0 0 500 630">
            <defs>
                <filter id="glow"><feGaussianBlur stdDeviation="2.5" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
            </defs>
            
            <g stroke="white" stroke-width="1" opacity="0.05">
                <line x1="50" y1="90" x2="450" y2="90" /><line x1="50" y1="220" x2="450" y2="220" /><line x1="50" y1="350" x2="450" y2="350" />
                <line x1="200" y1="50" x2="200" y2="520" /><line x1="300" y1="50" x2="300" y2="520" />
            </g>

            <g fill="rgba(255,255,255,0.03)" stroke="rgba(255,255,255,0.1)">
                <rect x="70" y="70" width="70" height="40" rx="8" /><text x="92" y="95" fill="#64748b" font-size="12">L3</text>
                <rect x="360" y="70" width="70" height="40" rx="8" /><text x="382" y="95" fill="#64748b" font-size="12">R3</text>
                <rect x="70" y="200" width="70" height="40" rx="8" /><text x="92" y="225" fill="#64748b" font-size="12">L2</text>
                <rect x="360" y="200" width="70" height="40" rx="8" /><text x="382" y="225" fill="#64748b" font-size="12">R2</text>
                <rect x="70" y="330" width="70" height="40" rx="8" /><text x="92" y="355" fill="#64748b" font-size="12">L1</text>
                <rect x="360" y="330" width="70" height="40" rx="8" /><text x="382" y="355" fill="#64748b" font-size="12">R1</text>
            </g>

            <g id="slave_agv" style="transition: transform 1.5s ease-in-out;">
                <rect x="180" y="450" width="40" height="60" rx="10" fill="#fb7185" filter="url(#glow)" />
                <text x="194" y="485" fill="white" font-weight="bold">S</text>
            </g>
            <g id="master_agv" style="transition: transform 1.5s ease-in-out;">
                <rect x="280" y="450" width="40" height="60" rx="10" fill="#38bdf8" filter="url(#glow)" />
                <text x="294" y="485" fill="white" font-weight="bold">M</text>
            </g>
        </svg>

        <script>
            if ({str(st.session_state.mission_trigger).lower()}) {{
                const agv = document.getElementById("{svg_id}");
                
                // Step-by-Step Multi-Axis Animation
                // 1. Move Vertically to Aisle
                agv.style.transform = "translateY({target_dy}px)";
                
                // 2. Turn & Move Horizontally to Rack
                setTimeout(() => {{
                    agv.style.transform = "translateY({target_dy}px) translateX({target_dx}px)";
                }}, 1600);
                
                // 3. Wait 2s at Rack, then Return Horizontally
                setTimeout(() => {{
                    agv.style.transform = "translateY({target_dy}px) translateX(0px)";
                }}, 5000);
                
                // 4. Return Vertically to Dock
                setTimeout(() => {{
                    agv.style.transform = "translateY(0px) translateX(0px)";
                }}, 6600);
            }}
        </script>
    </div>
    """
    components.html(html_map, height=670)

if st.session_state.mission_trigger:
    st.session_state.mission_trigger = False
