import matplotlib.pyplot as plt
import numpy as np

# Data for the graph
labels = ['Direct On-Chain Storage\n(Prior Work)', 'MedScan AI Pipeline\n(IPFS Off-Chain)']
# Storing 500KB raw data costs ~12.5M Gas vs storing a CID ~238k Gas
# NOTE: Using slightly lower actual gas (e.g., ~135k) is more typical
# for CID storage, but we can use the Ganache number too.
gas_costs = [12500000, 238365] 

fig, ax = plt.subplots(figsize=(8, 6))

# Plot the bar chart
# Using contrasting colors
bars = ax.bar(labels, gas_costs, color=['#ef4444', '#10b981'], width=0.5, edgecolor='black')

# Using a LOGARITHMIC scale because the difference is so massive!
# Otherwise, the second bar would be too small to see.
ax.set_yscale('log')
ax.set_ylim(10000, 100000000) # Set range of Y axis (10k to 100M)

# Add chart labels and title
ax.set_ylabel('Gas Units Consumed (Logarithmic Scale)', fontsize=12, fontweight='bold')
ax.set_title('Blockchain Storage Optimization: Direct Raw Data vs. CID Indexing', fontsize=14, fontweight='bold', pad=15)

# Add the specific gas number on top of the bars
for bar in bars:
    yval = bar.get_height()
    # For a log scale, positioning the text requires multiplying, not adding
    ax.text(bar.get_x() + bar.get_width()/2, yval * 1.15, f'{int(yval):,} Gas', 
            ha='center', va='bottom', fontsize=12, fontweight='bold')

plt.tight_layout()
# plt.show() # Uncomment this if you want to see the graph popup
plt.savefig('gas_cost_comparison.png', dpi=300) # Saves the graph as a high-res image
print("Successfully generated gas_cost_comparison.png")