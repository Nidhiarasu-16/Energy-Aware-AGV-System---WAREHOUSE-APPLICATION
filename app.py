import streamlit as st
import streamlit.components.v1 as components

# --- Page Config ---
st.set_page_config(page_title="Intelligent AGV Control", layout="wide")

# --- CSS: Large Text, Big Energy Bars, and Dark Aesthetics ---
st.markdown("""
    <style>
    .stApp { background: #060d17; }
    
    /* 1. HUGE DROPDOWNS & TEXT */
    .stSelectbox label p { font-size: 28px !important; font-weight: bold !important; color: #cbd5e1 !important; }
    div[data-baseweb="select"] > div { font-size: 24px !important; height: 65px !important; background: rgba(255,255,255,0.05) !important; color: white !important; }
    
    /* 2. LARGE GAUGE-STYLE ENERGY BARS */
    .energy-card { background: rgba(255,255,255,0.03); padding: 20px; border-radius: 15px; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 20px; }
    .energy-label { font-size: 22px; font-weight: bold; color: #94a3b8; margin-bottom: 10px; display: block; }
    .bar-bg { width: 100%; background: #1e293b; height: 35px; border-radius: 8px; overflow: hidden; position: relative; border: 1px solid #334155; }
    .bar-fill { height: 100%; display: flex; align-items: center; justify-content: flex-end; padding-right: 15px; color: white; font-weight: bold; font-size: 18px; transition: width 1s; }

    /* 3. EXECUTE BUTTON */
    button[kind="primary"] { height: 80px !important; font-size: 26px !important; font-weight: bold !important; background: linear-gradient(90deg, #38bdf8, #818cf8) !important; border: none !important; border-radius: 15px !important; margin-top: 20px !important; }

    /* 4. STATUS BOX */
    .status-box { background: rgba(34, 197, 94, 0.1); border-left: 6px solid #22c55e; padding: 25px; border-radius: 12px; color: white; font-size: 22px; margin-top: 30px; }
    </style>
    """, unsafe_allow_html=True)

# --- Intelligence Logic ---
m_charge = 28
s_charge = 76

# Auto-select the hero of the mission
if s_charge >= m_charge:
    active_id, active_color, active_label = "slave_agv", "#fb7185", "Slave Unit (S)"
    start_x = 200
else:
    active_id, active_color, active_label = "master_agv", "#38bdf8", "Master Unit (M)"
    start_x = 300

RACK_MAP = {
    "L3": {"y": 90, "x": 110}, "R3": {"y": 90, "x": 395},
    "L2": {"y": 220, "x": 110}, "R2": {"y": 220, "x": 395},
    "L1": {"y": 350, "x": 110}, "R1": {"y": 350, "x": 395}
}

# --- Layout ---
col1, col2 = st.columns([1, 1.4], gap="large")

with col1:
    st.markdown('<h1 style="color:white; font-size: 42px;">System <span style="color:#38bdf8;">OS</span></h1>', unsafe_allow_html=True)
    
    # Energy Section
    st.markdown(f'''<div class="energy-card">
        <span class="energy-label">Master Energy</span>
        <div class="bar-bg"><div class="bar-fill" style="width: 28%; background: #38bdf8;">28%</div></div>
        <span class="energy-label">Slave Energy</span>
        <div class="bar-bg"><div class="bar-fill" style="width: 76%; background: #fb7185;">76%</div></div>
    </div>''', unsafe_allow_html=True)
    
    # Dropdowns
    rack_sel = st.selectbox("Target Rack Location", list(RACK_MAP.keys()), index=4)
    item_sel = st.selectbox("Inventory Item Selection", ["Bearing 10cm", "Gear 15cm", "Shaft 5cm"])
    
    # Trigger
    do_dispatch = st.button("EXECUTE MISSION", type="primary", use_container_width=True)

    st.markdown(f"""<div class="status-box">
        <b>MISSION CONTROL</b><br>
        Unit: {active_label}<br>
        Status: {"Dispatched" if do_dispatch else "Standby"}
    </div>""", unsafe_allow_html=True)

with col2:
    coords = RACK_MAP[rack_sel]
    dy = coords['y'] - 450
    dx = coords['x'] - start_x
    
    # Javascript trigger logic
    run_js = "true" if do_dispatch else "false"

    svg_html = f"""
    <div style="background: rgba(255,255,255,0.02); border-radius: 30px; padding: 20px; border: 1px solid rgba(255,255,255,0.05);">
        <svg width="100%" height="650" viewBox="0 0 500 630">
            <defs><filter id="glow"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
            
            <g stroke="white" stroke-width="1" opacity="0.05">
                <line x1="50" y1="90" x2="450" y2="90" /><line x1="50" y1="220" x2="450" y2="220" /><line x1="50" y1="350" x2="450" y2="350" />
                <line x1="200" y1="50" x2="200" y2="520" /><line x1="300" y1="50" x2="300" y2="520" />
            </g>

            <g fill="rgba(255,255,255,0.05)" stroke="rgba(255,255,255,0.2)">
                {" ".join([f'<rect x="{70 if k[0]=="L" else 360}" y="{v["y"]-20}" width="70" height="40" rx="5" />' for k,v in RACK_MAP.items()])}
                {" ".join([f'<text x="{"92" if k[0]=="L" else "382"}" y="{v["y"]+5}" fill="white" font-size="14">{k}</text>' for k,v in RACK_MAP.items()])}
            </g>

            <g id="slave_agv" style="transition: transform 1.2s ease-in-out;">
                <rect x="180" y="450" width="40" height="60" rx="10" fill="#fb7185" filter="url(#glow)" />
                <text x="194" y="488" fill="white" font-weight="bold">S</text>
            </g>
            <g id="master_agv" style="transition: transform 1.2s ease-in-out;">
                <rect x="280" y="450" width="40" height="60" rx="10" fill="#38bdf8" filter="url(#glow)" />
                <text x="294" y="488" fill="white" font-weight="bold">M</text>
            </g>
            
            <rect x="175" y="540" width="150" height="60" rx="15" fill="rgba(255,255,255,0.05)" />
            <text x="200" y="575" fill="#94a3b8" font-size="10" font-weight="bold">CHARGING BASE</text>
        </svg>

        <script>
            if ({run_js}) {{
                const unit = document.getElementById("{active_id}");
                
                // Force sync with the browser's refresh cycle to ensure outbound animation plays
                requestAnimationFrame(() => {{
                    requestAnimationFrame(() => {{
                        // 1. Outbound Vertical
                        unit.style.transform = "translateY({dy}px)";
                        
                        // 2. Outbound Horizontal (after vertical finishes)
                        setTimeout(() => {{
                            unit.style.transform = "translateY({dy}px) translateX({dx}px)";
                        }}, 1300);
                        
                        // 3. Return Horizontal (after 3s wait)
                        setTimeout(() => {{
                            unit.style.transform = "translateY({dy}px) translateX(0px)";
                        }}, 5000);
                        
                        // 4. Return Vertical (Home)
                        setTimeout(() => {{
                            unit.style.transform = "translateY(0px) translateX(0px)";
                        }}, 6300);
                    }});
                }});
            }}
        </script>
    </div>
    """
    components.html(svg_html, height=670)
