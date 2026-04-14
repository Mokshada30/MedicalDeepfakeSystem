import json
import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

hospital_addresses = {
    "Hospital_A": os.getenv("HOSPITAL_A_ADDRESS"),
    "Hospital_B": os.getenv("HOSPITAL_B_ADDRESS"),
    "Hospital_C": os.getenv("HOSPITAL_C_ADDRESS"),
    "Hospital_D": os.getenv("HOSPITAL_D_ADDRESS")
}

keystore = {}

# Generate a unique Fernet key for each address
for name, address in hospital_addresses.items():
    if address: 
        unique_key = Fernet.generate_key().decode()
        keystore[address] = unique_key
        print(f"Generated key for {name}")
    else:
        print(f"Warning: {name} address not found in .env file!")

with open("keystore.json", "w") as f:
    json.dump(keystore, f, indent=4)

print("\nSuccess! keystore.json has been created.")