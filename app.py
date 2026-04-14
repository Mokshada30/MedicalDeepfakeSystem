import streamlit as st
import os
import time
import numpy as np
import pandas as pd
from PIL import Image
import io
from main import process_scan, contract, ipfs, decrypt_scan 
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="MedScan AI Protocol", page_icon="🛡️", layout="wide")

if 'active_tab' not in st.session_state:
    st.session_state['active_tab'] = "Home"

st.sidebar.markdown("<h2 style='text-align: center;'>🏥 Network Node</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center; color: #94a3b8; font-size: 0.9rem;'>Simulate identity switching on the shared consortium ledger.</p>", unsafe_allow_html=True)

hospital_directory = {
    "Hospital A (Admin)": {
        "address": os.getenv("HOSPITAL_A_ADDRESS"),
        "key": os.getenv("HOSPITAL_A_KEY")
    },
    "Hospital B": {
        "address": os.getenv("HOSPITAL_B_ADDRESS"),
        "key": os.getenv("HOSPITAL_B_KEY")
    },
    "Hospital C": {
        "address": os.getenv("HOSPITAL_C_ADDRESS"),
        "key": os.getenv("HOSPITAL_C_KEY")
    }
}

active_hospital = st.sidebar.selectbox("Select Active Identity:", list(hospital_directory.keys()))

current_sender = hospital_directory[active_hospital]["address"]
current_key = hospital_directory[active_hospital]["key"]

st.sidebar.success(f"🟢 Connected as {active_hospital}")
st.sidebar.markdown("---")
st.sidebar.markdown("<div style='font-size: 0.8rem; color: #64748b;'>All hospitals interact with the same underlying smart contract, enforcing a single source of truth.</div>", unsafe_allow_html=True)

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
<div style="background-color: #0b1120; border: 1px solid #1e293b; border-left: 4px solid #38bdf8; border-radius: 8px; padding: 1.5rem; margin-top: 2rem;">
    <h4 style="color: #f8fafc; margin-top: 0; margin-bottom: 1rem; display: flex; align-items: center; gap: 8px;">
        🛡️ Enterprise Consortium Architecture
    </h4>
    <div style="display: flex; gap: 2rem; color: #94a3b8; font-size: 0.9rem;">
        <div style="flex: 1;">
            <strong style="color: #cbd5e1;">Consensus Mechanism:</strong> Proof of Authority (PoA)<br>
            <span style="font-size: 0.8rem;">Simulated via local RPC node.</span>
        </div>
        <div style="flex: 1;">
            <strong style="color: #cbd5e1;">Entry Validation:</strong> Smart Contract RBAC<br>
            <span style="font-size: 0.8rem;">Only cryptographically signed transactions from whitelisted clinical addresses are accepted.</span>
        </div>
        <div style="flex: 1;">
            <strong style="color: #cbd5e1;">51% Attack Defense:</strong> Immutable via Authority<br>
            <span style="font-size: 0.8rem;">Sybil and 51% compute attacks are mitigated as validation rights are tied to verified institutional identity, not hash power.</span>
        </div>
    </div>
</div>
    """, unsafe_allow_html=True)

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

            if st.button("Upload & Encrypt Data", type="primary", use_container_width=True):
                if not is_connected:
                    st.error("Cannot process: Ganache is offline. Please start your local blockchain.")
                else:
                    with st.spinner("Analyzing textures and Encrypting Payload..."):
                        verdict, conf, cid, tx_hash = process_scan(processing_path, current_sender, current_key)
                        
                        if verdict:
                            if verdict.lower() == 'fake':
                                st.error("🚨 Fraud Attempt Detected & Logged")
                                border_color = "#ef4444"
                                title_html = '<h4 style="color: #ef4444; margin-top: 0; margin-bottom: 1rem;">🚨 Malicious Payload Captured</h4>'
                            else:
                                st.success("✅ Analysis Complete & Encrypted")
                                border_color = "#334155"
                                title_html = ''

                            upload_success_html = f"""<div style="background-color: #1e293b; border: 1px solid {border_color}; border-radius: 12px; padding: 1.5rem; margin-top: 1rem; color: #f8fafc; font-size: 1rem;">
{title_html}
<p style="margin-bottom: 0.8rem;"><strong style="color:#94a3b8;">Encrypted Hash (CID):</strong> <code style="color:#38bdf8; background:transparent; font-size: 1rem;">{cid}</code></p>
<p style="margin-bottom: 0.8rem;"><strong style="color:#94a3b8;">Verdict:</strong> <span style="color:{'#ef4444' if verdict.lower()=='fake' else '#22c55e'}; font-weight:bold; font-size: 1.1rem;">{verdict}</span> ({conf}%)</p>
<p style="margin-bottom: 0;"><strong style="color:#94a3b8;">Blockchain TX:</strong> <code style="color:#38bdf8; background:transparent; font-size: 1rem;">{tx_hash}</code></p>
</div>"""
                            st.markdown(upload_success_html, unsafe_allow_html=True)
                        else:
                            st.error(f"❌ Blockchain Transaction Failed! Error: {tx_hash}")
                            st.warning("If this says 'Unauthorized', it means you need to go to Remix and authorize this hospital's address using the Admin account before you can upload.")

with tab_verify:
    st.markdown("<h2 style='text-align: center; padding-top: 2rem;'>Verify Scan Integrity</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color:#94a3b8;'>Enter the IPFS Hash to audit the record and decrypt the medical image.</p>", unsafe_allow_html=True)
    
    col_v1, col_v_main, col_v2 = st.columns([1, 4, 1])
    
    with col_v_main:
        search_hash = st.text_input("Enter Clinical Hash (CID)")
        if st.button("Audit & Decrypt Record", type="primary", use_container_width=True):
            if not is_connected:
                st.error("Cannot verify: Ganache is offline. Please start your local blockchain.")
            elif search_hash:
                history = get_history()
                match = next((r for r in history if r[0] == search_hash), None)
                if match:
                    # 1. The Blockchain Proof
                    verify_success_html = f"""<div style="background: #1e293b; border: 1px solid #22c55e; border-radius: 12px; padding: 2.5rem; text-align: center;">
<div style="font-size: 3rem; margin-bottom: 1rem;">✅</div>
<h2 style="color: white; margin: 0;">Integrity Confirmed</h2>
<p style="color: #94a3b8;">This scan matches the original clinical record stored on the blockchain.</p>

<div style="text-align: left; margin-top: 2rem; padding: 1.5rem; background-color: #0f172a; border-radius: 8px; border: 1px solid #334155; font-size: 1rem;">
<p style="margin-bottom: 0.8rem;"><strong style="color:#94a3b8;">Hash (CID):</strong> <code style="color:#38bdf8; background:transparent; font-size: 1rem;">{match[0]}</code></p>
<p style="margin-bottom: 0.8rem;"><strong style="color:#94a3b8;">Original AI Analysis:</strong> <strong style="color:white; font-size: 1.1rem;">{match[1]}</strong> <span style="color:white;">({match[2]}% Confidence)</span></p>
<p style="margin-bottom: 0;"><strong style="color:#94a3b8;">Smart Contract:</strong> <code style="color:#38bdf8; background:transparent; font-size: 1rem;">{contract.address}</code></p>
</div>
</div>"""
                    st.markdown(verify_success_html, unsafe_allow_html=True)

                    # 2. The Encryption Demo View
                    st.markdown("<h3 style='color: white; margin-top: 2rem; text-align: center;'>🔒 Cryptographic Verification</h3>", unsafe_allow_html=True)
                    
                    col_sec1, col_sec2 = st.columns(2)
                    
                    try:
                        # Fetch the raw scrambled data from IPFS
                        enc_data = ipfs.cat(search_hash)
                        
                        with col_sec1:
                            st.error("🚨 Attacker's View (Raw IPFS Data)")
                            st.markdown("<p style='font-size: 0.85rem; color: #94a3b8;'>What a malicious actor sees if they intercept the public IPFS Hash.</p>", unsafe_allow_html=True)
                            
                            # Show a snippet of the scrambled data
                            st.code(str(enc_data[:300]) + "...\n\n[DATA UNREADABLE]", language="text")
                            
                        with col_sec2:
                            st.success("🏥 Hospital View (Decrypted)")
                            st.markdown("<p style='font-size: 0.85rem; color: #94a3b8;'>Using the secure environment key, the payload is fully restored.</p>", unsafe_allow_html=True)
                            
                            # Decrypt it using the helper function
                            decrypted_bytes = decrypt_scan(enc_data)
                            
                            if decrypted_bytes:
                                # Convert the bytes back to a viewable image
                                verified_img = Image.open(io.BytesIO(decrypted_bytes))
                                st.image(verified_img, caption="Restored Medical Scan", use_container_width=True)
                            else:
                                st.error("Decryption Failed: Invalid or missing Private Key.")
                                
                    except Exception as e:
                        st.error(f"IPFS Retrieval Failed. Is your local IPFS node running? Error: {e}")
                else:
                    st.error("Audit Failed: No matching record found in the Blockchain.")
            else:
                st.warning("Please enter a Hash to verify.")