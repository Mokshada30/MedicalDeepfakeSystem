# Blockchain based Verification System for Forged Medical Images

A decentralized, end-to-end medical deepfake detection system. This project integrates Deep Learning (PyTorch) for microscopic forgery detection with Web3 technologies (Ethereum/IPFS) to create an immutable, tamper-proof audit trail for medical scans.

## Features
* **AI-Powered Detection:** Utilizes a custom-trained ResNet-50 Convolutional Neural Network to detect GAN-generated deepfakes in MRI and CT scans.
* **Decentralized Storage:** Scans are hashed and pinned to the InterPlanetary File System (IPFS), ensuring the source file cannot be altered.
* **Immutable Audit Trail:** Verification results, confidence scores, and IPFS CIDs are notarized via a Solidity smart contract on a local Ethereum blockchain.
* **Interactive UI:** A fully functional Streamlit frontend allowing users to upload scans and view real-time AI and Blockchain verification metrics.

## Tech Stack
* **Machine Learning:** PyTorch, Torchvision, NumPy, PIL
* **Blockchain & Storage:** Solidity, Web3.py, Ganache, IPFS Desktop
* **Frontend:** Streamlit

## Project Structure
```text
MedicalDeepfakeSystem/
│
├── blockchain_layer/
│   ├── ABI.json                  # Smart contract interface
│   └── MedicalAudit.sol          # Solidity contract source code
│
├── ml_layer/
│   ├── detector.py               # ResNet-50 inference logic
│   └── medical_deepfake_resnet50_ULTIMATE.pth # Trained weights (Excluded via Gitignore)
│
├── training/
│   └── Medical_Deepfake_Training_ResNet50.ipynb # Original Colab training script
│
├── app.py                        # Streamlit web interface
├── main.py                       # Core pipeline routing (AI -> IPFS -> Blockchain)
├── requirements.txt              # Python dependencies
└── README.md
```
## How to Run Locally
1. Prerequisites

    Ensure you have Python 3.10+, Ganache, and IPFS Desktop installed and running.

2. Setup Virtual Environment

    Bash
    ```text
    python -m venv venv
    source venv/Scripts/activate  # On Windows
    pip install -r requirements.txt
    ```
3. Blockchain Configuration

    Deploy MedicalAudit.sol using Remix IDE to your local Ganache network.

    Copy the deployed contract address and update the CONTRACT_ADDRESS variable in main.py.

4. Launch the Application

    Bash
    ```text
    streamlit run app.py
    ```
Upload a .png, .jpg, or .npy file through the browser interface to initiate the verification pipeline.

## Model Training Details
The core detection model is a ResNet-50 architecture utilizing transfer learning. It was fine-tuned to identify subtle pixel artifacts left by CT-GANs and other medical image manipulation frameworks. To view the data augmentation strategy and training loop, refer to the Jupyter Notebook located in the training/ directory.

*Developed as a Major Project Submission.*