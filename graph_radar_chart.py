import matplotlib.pyplot as plt
import numpy as np

# Metrics and Data
labels = np.array(['Accuracy', 'Precision', 'Recall', 'F1-Score', 'Specificity'])
num_vars = len(labels)

# Real data from the papers
mastoi_scores = [96.54, 95.82, 96.12, 95.96, 96.80]
yolo_scores = [86.6, 85.0, 82.0, 83.4, 88.1]
medscan_scores = [97.56, 95.24, 100.0, 97.56, 95.12] 

# Computing angles for the radar chart layout
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

# The plot needs to be circular, so we "complete the loop" by appending the first value to the end
mastoi_scores += mastoi_scores[:1]
yolo_scores += yolo_scores[:1]
medscan_scores += medscan_scores[:1]
angles += angles[:1]

fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

# Draw one axe per variable and add labels
plt.xticks(angles[:-1], labels, color='black', size=12, fontweight='bold')

# Draw ylabels
ax.set_rlabel_position(30)
plt.yticks([80, 85, 90, 95, 100], ["80", "85", "90", "95", "100"], color="grey", size=10)
plt.ylim(75, 105)

# Plot YOLO
ax.plot(angles, yolo_scores, linewidth=2, linestyle='dashed', label='YOLOv5 (Prior)', color='#f59e0b')
ax.fill(angles, yolo_scores, '#f59e0b', alpha=0.1)

# Plot Mastoi
ax.plot(angles, mastoi_scores, linewidth=2, linestyle='dotted', label='Mastoi et al. (Prior)', color='#94a3b8')

# Plot Proposed MedScan
ax.plot(angles, medscan_scores, linewidth=3, linestyle='solid', label='MedScan AI (Proposed)', color='#10b981')
ax.fill(angles, medscan_scores, '#10b981', alpha=0.25)

plt.title('Holistic Deep Learning Performance Comparison', size=15, fontweight='bold', y=1.1)
plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))

plt.tight_layout()
plt.savefig('radar_comparison.png', dpi=300)
print("Graph saved as radar_comparison.png")