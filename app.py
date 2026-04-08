import streamlit as st
import os
import numpy as np
import pandas as pd
from PIL import Image
from main import process_scan, contract, ipfs

st.set_page_config(page_title="MedScan AI Protocol", page_icon="🛡️", layout="wide")

if 'active_tab' not in st.session_state:
    st.session_state['active_tab'] = "Home"

st.markdown("""
<style>
    .stApp { background-color: #0f172a; }
    
    .stTabs [data-baseweb="tab-list"] {
        display: flex;
        justify-content: flex-end;
        margin-top: -60px; 
        margin-right: 220px; 
        border-bottom: none;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #94a3b8 !important;
        font-weight: 600;
        background-color: transparent !important;
        gap: 5px;
    }
    .stTabs [aria-selected="true"] { color: #a78bfa !important; border-bottom: 2px solid #a78bfa !important; }

    .hero-container { text-align: center; padding: 3rem 0; }
    .hero-title {
        font-size: 3.5rem; font-weight: 800;
        background: linear-gradient(to right, #a78bfa, #8b5cf6);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    .hero-subtitle { color: #94a3b8; font-size: 1.1rem; margin-bottom: 2rem; }

    .stat-card {
        background-color: #1e293b; border: 1px solid #334155;
        border-radius: 12px; padding: 1.5rem; text-align: left; height: 100%;
    }
    .stat-number { font-size: 2.2rem; font-weight: 700; color: #a78bfa; margin-bottom: 5px; }
    .stat-label { color: #94a3b8; font-size: 0.9rem; }

    .feature-card {
        background-color: #1e293b; border: 1px solid #334155;
        border-radius: 12px; padding: 1.5rem; margin-top: 2rem; min-height: 200px;
    }
    
    .hiw-container {
        background-color: #1e293b; border: 1px solid #334155;
        border-radius: 12px; padding: 2.5rem; margin-top: 3rem; margin-bottom: 2rem;
    }
    .step-circle {
        background: #8b5cf6; color: white; width: 45px; height: 45px;
        border-radius: 50%; display: flex; align-items: center; justify-content: center;
        margin: 0 auto 10px; font-weight: 800; font-size: 1.1rem;
    }
    
    [data-testid="stDataFrame"] { border: 1px solid #334155; border-radius: 12px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)

def get_history():
    try: 
        return contract.functions.getAllReports().call()
    except: 
        return []

try:
    contract.functions.getAllReports().call()
    is_connected = True
    status_color = "#22c55e"
    status_text = "Blockchain Connected"
    card_icon = "✔️"
except:
    is_connected = False
    status_color = "#ef4444"
    status_text = "Blockchain Offline"
    card_icon = "❌"

st.markdown('<div style="font-size: 1.6rem; font-weight: 800; color: white; margin-top: -10px;">🛡️ MedScan AI</div>', unsafe_allow_html=True)
st.markdown(f'<div style="position: absolute; top: -42px; right: 20px; color: #94a3b8; font-weight: 600; font-size: 1rem; display: flex; align-items: center; gap: 8px;"><div style="width: 10px; height: 10px; background-color: {status_color}; border-radius: 50%; box-shadow: 0 0 8px {status_color};"></div> {status_text}</div>', unsafe_allow_html=True)

tabs = ["🏠 Home", "☁️ Upload", "✔️ Verify"]
tab_home, tab_upload, tab_verify = st.tabs(tabs)

with tab_home:
    st.markdown('<div class="hero-container"><div class="hero-title">AI-Powered Medical Scan Verification</div><div class="hero-subtitle">Secure, tamper-proof medical scan verification powered by artificial intelligence and blockchain technology.</div></div>', unsafe_allow_html=True)

    history = get_history()
    total = len(history)
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.markdown(f'<div class="stat-card"><div class="stat-number">{total}</div><div class="stat-label">Total Scans</div></div>', unsafe_allow_html=True)
    with m2: st.markdown(f'<div class="stat-card"><div class="stat-number">{total}</div><div class="stat-label">On-Chain Registered</div></div>', unsafe_allow_html=True)
    with m3: st.markdown(f'<div class="stat-card"><div class="stat-number">{card_icon}</div><div class="stat-label">{status_text}</div></div>', unsafe_allow_html=True)
    with m4: st.markdown('<div class="stat-card"><div class="stat-number">🤖</div><div class="stat-label">AI Processing</div></div>', unsafe_allow_html=True)

    f1, f2, f3 = st.columns(3)
    with f1: st.markdown('<div class="feature-card"><div style="font-size: 1.5rem; margin-bottom: 10px;">🧠</div><h4 style="color: white; margin-top:0;">AI Analysis</h4><p style="color:#94a3b8;">Advanced ResNet-50 texture analysis detect microscopic artifacts in MRI/CT slices.</p></div>', unsafe_allow_html=True)
    with f2: st.markdown('<div class="feature-card"><div style="font-size: 1.5rem; margin-bottom: 10px;">🔗</div><h4 style="color: white; margin-top:0;">Blockchain Security</h4><p style="color:#94a3b8;">Cryptographic hashes stored on Ethereum ensure clinical data remains immutable.</p></div>', unsafe_allow_html=True)
    with f3: st.markdown('<div class="feature-card"><div style="font-size: 1.5rem; margin-bottom: 10px;">🏥</div><h4 style="color: white; margin-top:0;">Privacy First</h4><p style="color:#94a3b8;">Patient PII never leaves local storage. Only tamper-proof hashes are recorded on-chain.</p></div>', unsafe_allow_html=True)

    st.markdown("""
<div class="hiw-container">
    <div style="color: white; font-weight: 700; font-size: 1.2rem; margin-bottom: 2rem;">🟢 How It Works</div>
    <div style="display: flex; justify-content: space-between; text-align: center;">
        <div style="flex: 1;"><div class="step-circle">1</div><div style="color: white; font-weight: 600;">Upload</div><div style="color: #94a3b8; font-size: 0.85rem;">Input DICOM/NPY slice</div></div>
        <div style="flex: 1;"><div class="step-circle">2</div><div style="color: white; font-weight: 600;">AI Analysis</div><div style="color: #94a3b8; font-size: 0.85rem;">ResNet-50 texture scan</div></div>
        <div style="flex: 1;"><div class="step-circle">3</div><div style="color: white; font-weight: 600;">Blockchain</div><div style="color: #94a3b8; font-size: 0.85rem;">Record hash on Ethereum</div></div>
        <div style="flex: 1;"><div class="step-circle">4</div><div style="color: white; font-weight: 600;">Verify</div><div style="color: #94a3b8; font-size: 0.85rem;">Audit via Verify tab</div></div>
    </div>
</div>
    """, unsafe_allow_html=True)

    st.markdown("<h3 style='color: white;'>🕒 Recent Scans</h3>", unsafe_allow_html=True)
    if is_connected and total > 0:
        df = pd.DataFrame([{"Document Hash (CID)": r[0][:25]+"...", "Type": "Medical Scan", "Status": "✅ Registered", "Confidence": f"{r[2]}%", "Verdict": r[1]} for r in reversed(history)])
        st.dataframe(df, use_container_width=True, hide_index=True)
    elif not is_connected:
        st.error("Cannot load history: Blockchain is offline.")
    else:
        st.info("No documents registered yet.")

with tab_upload:
    st.markdown("<h2 style='text-align: center; padding-top: 2rem;'>Scan Analysis & Registration</h2>", unsafe_allow_html=True)
    col_u1, col_u_main, col_u2 = st.columns([1, 2, 1])
    with col_u_main:
        uploaded_file = st.file_uploader("Select NPY or Image Scan", type=['png', 'jpg', 'jpeg', 'npy'])
        if uploaded_file:
            temp_path = os.path.join("datasets", uploaded_file.name)
            with open(temp_path, "wb") as f: f.write(uploaded_file.getbuffer())

            if uploaded_file.name.endswith(".npy"):
                data = np.load(temp_path)
                data_norm = ((data - data.min()) / (data.max() - data.min()) * 255).astype(np.uint8)
                img = Image.fromarray(data_norm)
                st.image(img, caption="NPY Slice Preview", use_container_width=True)
                processing_path = temp_path.replace(".npy", ".png")
                img.save(processing_path)
            else:
                st.image(uploaded_file, use_container_width=True)
                processing_path = temp_path

            if st.button("Upload", type="primary", use_container_width=True):
                if not is_connected:
                    st.error("Cannot process: Ganache is offline. Please start your local blockchain.")
                else:
                    with st.spinner("Analyzing textures..."):
                        verdict, conf, cid, tx_hash = process_scan(processing_path)
                        if verdict:
                            st.success("✅ Analysis Complete")
                            upload_success_html = f"""<div class="stat-card" style="margin-top: 1rem; height: auto; color: #f8fafc; font-size: 1rem;">
<p style="margin-bottom: 0.8rem;"><strong style="color:#94a3b8;">Hash:</strong> <code style="color:#38bdf8; background:transparent; font-size: 1rem;">{cid}</code></p>
<p style="margin-bottom: 0.8rem;"><strong style="color:#94a3b8;">Verdict:</strong> <span style="color:{'#ef4444' if verdict=='Fake' else '#22c55e'}; font-weight:bold; font-size: 1.1rem;">{verdict}</span> ({conf}%)</p>
<p style="margin-bottom: 0;"><strong style="color:#94a3b8;">TX:</strong> <code style="color:#38bdf8; background:transparent; font-size: 1rem;">{tx_hash}</code></p>
</div>"""
                            st.markdown(upload_success_html, unsafe_allow_html=True)

with tab_verify:
    st.markdown("<h2 style='text-align: center; padding-top: 2rem;'>Verify Scan Integrity</h2>", unsafe_allow_html=True)
    col_v1, col_v_main, col_v2 = st.columns([1, 2, 1])
    with col_v_main:
        search_hash = st.text_input("Enter Clinical Hash (CID)")
        if st.button("Verify Integrity", type="primary", use_container_width=True):
            if not is_connected:
                st.error("Cannot verify: Ganache is offline. Please start your local blockchain.")
            elif search_hash:
                history = get_history()
                match = next((r for r in history if r[0] == search_hash), None)
                if match:
                    verify_success_html = f"""<div style="background: #1e293b; border: 1px solid #22c55e; border-radius: 12px; padding: 2.5rem; text-align: center;">
<div style="font-size: 3rem; margin-bottom: 1rem;">✅</div>
<h2 style="color: white; margin: 0;">Integrity Confirmed</h2>
<p style="color: #94a3b8;">This scan matches the original clinical record.</p>

<div style="text-align: left; margin-top: 2rem; padding: 1.5rem; background-color: #0f172a; border-radius: 8px; border: 1px solid #334155; font-size: 1rem;">
<p style="margin-bottom: 0.8rem;"><strong style="color:#94a3b8;">Hash:</strong> <code style="color:#38bdf8; background:transparent; font-size: 1rem;">{match[0]}</code></p>
<p style="margin-bottom: 0.8rem;"><strong style="color:#94a3b8;">Original AI Analysis:</strong> <strong style="color:white; font-size: 1.1rem;">{match[1]}</strong> <span style="color:white;">({match[2]}% Confidence)</span></p>
<p style="margin-bottom: 0;"><strong style="color:#94a3b8;">Smart Contract:</strong> <code style="color:#38bdf8; background:transparent; font-size: 1rem;">{contract.address}</code></p>
</div>
</div>"""
                    st.markdown(verify_success_html, unsafe_allow_html=True)
                else:
                    st.error("Audit Failed: No matching record found in the Blockchain.")
            else:
                st.warning("Please enter a Hash to verify.")