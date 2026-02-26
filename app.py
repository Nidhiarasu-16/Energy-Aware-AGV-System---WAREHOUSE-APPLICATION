import streamlit as st
import streamlit.components.v1 as components

# --- Page Config ---
st.set_page_config(page_title="AGV Control Center", layout="wide")

# --- Modern Aesthetic CSS ---
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    }

    /* Glassmorphism Cards */
    .control-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 24px;
        padding: 30px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
    }

    /* Modern Energy Meters */
    .energy-header {
        color: #94a3b8;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 8px;
    }
    .energy-bar-bg {
        width: 100%;
        background: rgba(255,255,255,0.1);
        height: 12px;
        border-radius: 6px;
        overflow: hidden;
        margin-bottom: 25px;
    }
    .energy-bar-fill {
        height: 100%;
        border-radius: 6px;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.5);
        transition: width 1s ease-in-out;
    }

    /* Styled Dropdowns */
    .stSelectbox label p {
        color: #f8fafc !important;
        font-size: 18px !important;
        font-weight: 500 !important;
    }
    div[data-baseweb="select"] {
        background-color: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 12px !important;
        color: white !important;
    }

    /* Glowing Execute Button */
    button[kind="primary"] {
        background: linear-gradient(90deg, #ef4444, #f87171) !important;
        border: none !important;
        height: 60px !important;
        border-radius: 15px !important;
        font-weight: bold !important;
        font-size: 20px !important;
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.3) !important;
    }

    /* Clean Status Box */
    .status-container {
        border-left: 5px solid #22c55e;
        background: rgba(34, 197, 94, 0.1);
        padding: 20px;
        border-radius: 12px;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Logic ---
if 'mission_active' not in st.session_state:
    st.session_state.mission_active = False

RACK_Y = {"L3": 90, "R3": 90, "L2": 220, "R2": 220, "L1": 350, "R1": 350}

col1, col2 = st.columns([1, 1.4], gap="large")

with col1:
    st.markdown('<h1 style="color:white; font-size: 2.5rem; margin-bottom:1rem;">Command <span style="color:#38bdf8;">Center</span></h1>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="control-card">', unsafe_allow_html=True)
        
        # Energy Section
        st.markdown('<div class="energy-header">Master Unit Energy</div>', unsafe_allow_html=True)
        st.markdown('<div class="energy-bar-bg"><div class="energy-bar-fill" style="width: 28%; background: #38bdf8;"></div></div>', unsafe_allow_html=True)
        
        st.markdown('<div class="energy-header">Slave Unit Energy</div>', unsafe_allow_html=True)
        st.markdown('<div class="energy-bar-bg"><div class="energy-bar-fill" style="width: 76%; background: #fb7185;"></div></div>', unsafe_allow_html=True)
        
        # Dropdowns
        rack = st.selectbox("Destination Rack", ["L1", "L2", "L3", "R1", "R2", "R3"], index=4)
        product = st.selectbox("Inventory Item", ["Bearing 10cm", "Gear 15cm", "Shaft 5cm"], index=0)
        
        if st.button("EXECUTE MISSION", type="primary", use_container_width=True):
            st.session_state.mission_active = True
            
        st.markdown('</div>', unsafe_allow_html=True)

    # Status Box
    agv_type = "Slave (Red)" if rack.startswith("L") else "Master (Blue)"
    st.markdown(f"""
        <div class="status-container">
            <span style="color:#22c55e; font-weight:bold; font-size:14px; text-transform:uppercase;">Operation Logs</span><br>
            <span style="color:white; font-size:18px;"><b>Unit:</b> {agv_type}</span><br>
            <span style="color:white; font-size:18px;"><b>Task:</b> Retrieving {product}</span>
        </div>
    """, unsafe_allow_html=True)

with col2:
    active_agv = "slave_agv" if rack.startswith("L") else "master_agv"
    target_y = RACK_Y[rack] - 450
    move_trigger = "true" if st.session_state.mission_active else "false"

    svg_map = f"""
    <div style="background: rgba(255,255,255,0.03); border-radius: 30px; padding: 20px; border: 1px solid rgba(255,255,255,0.1);">
        <svg width="100%" height="650" viewBox="0 0 500 630">
            <defs>
                <filter id="glow">
                    <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
                    <feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge>
                </filter>
            </defs>
            
            <g stroke="white" stroke-width="1" opacity="0.1">
                <line x1="50" y1="90" x2="450" y2="90" />
                <line x1="50" y1="220" x2="450" y2="220" />
                <line x1="50" y1="350" x2="450" y2="350" />
            </g>

            <line x1="200" y1="50" x2="200" y2="520" stroke="#fb7185" stroke-width="3" opacity="0.6" />
            <line x1="300" y1="50" x2="300" y2="520" stroke="#38bdf8" stroke-width="3" opacity="0.6" />

            <g fill="rgba(255,255,255,0.05)" stroke="rgba(255,255,255,0.2)">
                <rect x="70" y="70" width="70" height="40" rx="8" /> <text x="92" y="95" fill="white" font-size="12" font-family="sans-serif">L3</text>
                <rect x="360" y="70" width="70" height="40" rx="8" /> <text x="382" y="95" fill="white" font-size="12" font-family="sans-serif">R3</text>
                <rect x="70" y="200" width="70" height="40" rx="8" /> <text x="92" y="225" fill="white" font-size="12" font-family="sans-serif">L2</text>
                <rect x="360" y="200" width="70" height="40" rx="8" /> <text x="382" y="225" fill="white" font-size="12" font-family="sans-serif">R2</text>
                <rect x="70" y="330" width="70" height="40" rx="8" /> <text x="92" y="355" fill="white" font-size="12" font-family="sans-serif">L1</text>
                <rect x="360" y="330" width="70" height="40" rx="8" /> <text x="382" y="355" fill="white" font-size="12" font-family="sans-serif">R1</text>
            </g>

            <g id="slave_agv" style="transition: transform 2.5s cubic-bezier(0.45, 0, 0.55, 1);">
                <rect x="180" y="450" width="40" height="60" rx="10" fill="#fb7185" filter="url(#glow)" />
                <text x="194" y="485" fill="white" font-weight="bold">S</text>
            </g>

            <g id="master_agv" style="transition: transform 2.5s cubic-bezier(0.45, 0, 0.55, 1);">
                <rect x="280" y="450" width="40" height="60" rx="10" fill="#38bdf8" filter="url(#glow)" />
                <text x="294" y="485" fill="white" font-weight="bold">M</text>
            </g>

            <rect x="170" y="540" width="160" height="60" rx="15" fill="rgba(255,255,255,0.05)" stroke="rgba(255,255,255,0.1)" />
            <text x="195" y="575" fill="#94a3b8" font-size="10" font-weight="bold" letter-spacing="1">DOCKING STATION</text>
        </svg>

        <script>
            if ({move_trigger}) {{
                const agv = document.getElementById("{active_agv}");
                window.requestAnimationFrame(() => {{
                    window.requestAnimationFrame(() => {{
                        agv.style.transform = "translateY({target_y}px)";
                        setTimeout(() => {{ agv.style.transform = "translateY(0px)"; }}, 5000);
                    }});
                }});
            }}
        </script>
    </div>
    """
    components.html(svg_map, height=670)

# Reset trigger
if st.session_state.mission_active:
    st.session_state.mission_active = False
