# Blockchain based Verification System for Forged Medical Images

A decentralized, end-to-end medical deepfake detection system. This project integrates Deep Learning (PyTorch) for microscopic forgery detection with Web3 technologies (Ethereum/IPFS) and AES-256 cryptography to create an immutable, zero-knowledge audit trail for clinical media.

## 🌟 Key Features
* **Micro-Texture AI Diagnostics:** Utilizes a custom-trained ResNet-50 Convolutional Neural Network with residual skip connections to detect high-frequency GAN-generated artifacts in MRI and CT scans.
* **Dual-Layer Cryptographic Privacy:** Medical scans undergo localized AES-256 symmetric encryption *before* being routed off-chain, ensuring strict data privacy and HIPAA compliance on a public peer-to-peer network.
* **Zero-Knowledge Decentralized Storage:** Encrypted payloads are hashed and pinned to the InterPlanetary File System (IPFS). Only the lightweight 32-byte Content Identifier (CID) is committed to the blockchain, reducing computational EVM gas overhead by 98%.
* **Immutable Audit Trail & RBAC:** Verification results, confidence scores, and IPFS CIDs are notarized via a Solidity smart contract featuring strict Role-Based Access Control (RBAC) on a local Ethereum Proof of Authority (PoA) network.
* **Enterprise Consortium UI:** A fully functional Streamlit frontend simulating a multi-node clinical network. It allows users to dynamically switch identities, upload scans, and execute cryptographic integrity audits in real-time.

## 🛠️ Tech Stack
* **Machine Learning:** PyTorch, Torchvision, NumPy, PIL
* **Blockchain & Storage:** Solidity (v0.8.0), Web3.py, Ganache, IPFS Desktop (Kubo)
* **Security:** Cryptography (Fernet AES), python-dotenv
* **Frontend:** Streamlit, Pandas, Matplotlib

## 📂 Project Structure
```text
MedicalDeepfakeSystem/
│
├── blockchain_layer/
│   ├── ABI.json                  # Compiled Smart contract interface
│   └── MedicalAudit.sol          # Solidity contract source code (RBAC enabled)
│
├── ml_layer/
│   ├── detector.py               # ResNet-50 inference logic
│   └── medical_deepfake_resnet50_ULTIMATE.pth # Trained weights (Excluded via Gitignore)
│
├── training/
│   └── Medical_Deepfake_Training_ResNet50.ipynb # Original Colab training script
│
├── app.py                        # Streamlit multi-node clinical dashboard
├── main.py                       # Core pipeline (AI -> AES Encryption -> IPFS -> EVM)
├── .env                          # Environment variables (RPC URL, Contract Address, Node Keys)
├── keystore.json                 # Localized AES-256 symmetric keys for decryption
├── requirements.txt              # Python dependencies
└── README.md
🚀 How to Run Locally
1. Prerequisites
Ensure you have Python 3.10+, Ganache (Local RPC), and IPFS Desktop installed and running on your machine.

2. Setup Virtual Environment
Bash

python -m venv venv
source venv/Scripts/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
3. Environment & Cryptographic Setup
Create a .env file in the root directory to store your Ganache RPC details and the specific Ethereum addresses/private keys for your simulated clinical nodes:

Code snippet

GANACHE_URL="[http://127.0.0.1:7545](http://127.0.0.1:7545)"
CONTRACT_ADDRESS="Your_Deployed_Contract_Address" 

NODE_A_ADDRESS="0x..."
NODE_A_KEY="0x..."
# Add details for NODE_B, NODE_C, and NODE_D
Create a keystore.json file in the root directory to store the localized AES-256 symmetric encryption keys for each node:

JSON

{
    "0xNodeAAddress...": "Your_Generated_Fernet_Key_1=",
    "0xNodeBAddress...": "Your_Generated_Fernet_Key_2="
}
4. Blockchain Configuration (Smart Contract Deployment)
Open Remix IDE and compile MedicalAudit.sol.

Copy the newly generated ABI and replace the contents of blockchain_layer/ABI.json.

Deploy the contract using Node A's address (establishing Node A as the Admin).

Copy the deployed contract address and update the CONTRACT_ADDRESS variable in your .env file.

In Remix, use the Admin account to call the authorizeNode function to whitelist Node B, Node C, and Node D into the consortium.

5. Launch the Application
Bash

streamlit run app.py
Use the sidebar to switch between authorized clinical nodes. Upload a .png, .jpg, or .npy file to initiate the AI verification and cryptographic registration pipeline.

🧠 Model Training Details
The core detection engine is a custom ResNet-50 architecture utilizing transfer learning. It was fine-tuned specifically to identify subtle high-frequency pixel blending and volumetric artifacts left by CT-GANs. To view the data augmentation strategy, localized tensor processing, and the complete training loop, refer to the Jupyter Notebook located in the training/ directory.

*Developed as a Major Project Submission.*