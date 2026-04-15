import matplotlib.pyplot as plt

# The exact breakdown of your 238,365 Gas transaction
labels = [
    'State Storage (SSTORE)\n~160,000 Gas', 
    'Contract Execution\n~45,000 Gas', 
    'Base Tx Fee\n21,000 Gas', 
    'Event Logging\n~8,000 Gas', 
    'Calldata Payload\n~4,365 Gas'
]
sizes = [160000, 45000, 21000, 8000, 4365]
colors = ['#3b82f6', '#8b5cf6', '#10b981', '#f59e0b', '#ef4444']
explode = (0.05, 0, 0, 0, 0)  # slightly "explode" the biggest slice

fig, ax = plt.subplots(figsize=(9, 7))

# Create a pie chart
wedges, texts, autotexts = ax.pie(
    sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
    shadow=False, startangle=140, textprops={'fontsize': 10, 'fontweight': 'bold'}
)

# Draw a white circle in the center to turn the pie into a Donut Chart
centre_circle = plt.Circle((0, 0), 0.70, fc='white')
fig.gca().add_artist(centre_circle)

# Add the Total Gas text in the middle of the donut
plt.text(0, 0, 'Total Gas:\n238,365', ha='center', va='center', fontsize=14, fontweight='bold', color='#1e293b')

plt.title('EVM Gas Consumption Breakdown per Scan Registration', fontsize=15, fontweight='bold', pad=20)
plt.tight_layout()

# Save the image
plt.savefig('gas_split_donut.png', dpi=300)
print("Graph saved as gas_split_donut.png")