import matplotlib.pyplot as plt
import numpy as np

# Simulate 20 transactions
transactions = np.arange(1, 21)

# UPDATE: Simulating realistic EVM fluctuation between 190k and 240k 
# based on the empirical data from your Ganache logs.
actual_gas_used = np.random.uniform(190000, 240000, 20)

# Calculate the 20% safety buffer limit programmed into your Python backend
gas_limit = actual_gas_used * 1.2

plt.figure(figsize=(10, 6))
plt.plot(transactions, gas_limit, label='Dynamic Gas Limit (Allocated)', linestyle='--', color='#ef4444', marker='o')
plt.bar(transactions, actual_gas_used, label='Actual Gas Consumed', color='#3b82f6', alpha=0.7)

plt.title('EVM Gas Consumption: Actual Usage vs. Dynamic Limit', fontsize=14, fontweight='bold')
plt.xlabel('Sequential Diagnostic Transactions', fontsize=12)
plt.ylabel('Computational Gas Units', fontsize=12)
plt.xticks(transactions)

# Set Y-axis to comfortably fit the numbers
plt.ylim(0, 320000) 

plt.legend(loc='lower right')
plt.grid(axis='y', linestyle='--', alpha=0.6)

plt.tight_layout()
plt.savefig('gas_usage_chart.png', dpi=300)
print("Graph saved! (Updated to reflect 190k-240k EVM fluctuation)")