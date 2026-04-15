import matplotlib.pyplot as plt

# The Data
methods = ['Direct On-Chain Storage\n(Prior Work)', 'MedScan AI Pipeline\n(IPFS Off-Chain)']
# Storing a 500KB image on Ethereum costs ~8-15 million gas. Storing a 32-byte CID costs ~135k.
gas_costs = [12500000, 135000] 

fig, ax = plt.subplots(figsize=(8, 6))
bars = ax.bar(methods, gas_costs, color=['#ef4444', '#10b981'], width=0.5, edgecolor='black')

# Using a logarithmic scale because the on-chain cost is astronomically high
ax.set_yscale('log')

# FIX 1: Manually set the Y-axis limit higher (up to 100 million) to create "headroom"
ax.set_ylim(10000, 100000000)

ax.set_ylabel('Gas Units Consumed (Logarithmic Scale)', fontsize=12)

# FIX 2: Added 'pad=20' to push the title further up from the graph area
ax.set_title('Blockchain Transaction Overhead Comparison', fontsize=14, fontweight='bold', pad=20)

# Adding the exact numbers on top of the bars
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval * 1.25, f'{int(yval):,} Gas', 
            ha='center', va='bottom', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig('gas_cost_comparison.png', dpi=300)
print("Graph saved as gas_cost_comparison.png")