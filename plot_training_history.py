import matplotlib.pyplot as plt
import seaborn as sns

epochs = list(range(1, 26))
accuracy = [
    63.24, 66.67, 67.05, 67.43, 70.48, 77.90, 79.05, 78.48, 89.33, 89.33,
    89.90, 89.71, 92.95, 93.33, 92.57, 94.29, 91.05, 92.76, 92.38, 94.86,
    94.10, 95.62, 93.33, 94.67, 95.05
]
loss = [
    0.6442, 0.5821, 0.5698, 0.5918, 0.5451, 0.4309, 0.4239, 0.4449, 0.2937, 0.3039,
    0.2429, 0.2324, 0.2043, 0.1993, 0.1877, 0.1469, 0.2084, 0.1655, 0.1693, 0.1510,
    0.1581, 0.1473, 0.1529, 0.1455, 0.1413
]


sns.set_theme(style="whitegrid")

#Accuracy over Epochs
plt.figure(figsize=(8, 5))
plt.plot(epochs, accuracy, marker='o', linestyle='-', color='b', linewidth=2, markersize=5)
plt.title('ResNet-50 Training Accuracy over 25 Epochs', fontsize=14, fontweight='bold')
plt.xlabel('Epoch', fontsize=12)
plt.ylabel('Accuracy (%)', fontsize=12)
plt.xticks(range(1, 26, 2)) 
plt.ylim(60, 100)

plt.axhline(y=95.62, color='r', linestyle='--', alpha=0.7, label='Peak Accuracy (95.62%)')
plt.legend(loc='lower right')
plt.tight_layout()
plt.savefig('training_accuracy_graph.png', dpi=300)
print("✅ Saved training_accuracy_graph.png")
plt.close()

#Loss over Epochs
plt.figure(figsize=(8, 5))
plt.plot(epochs, loss, marker='s', linestyle='-', color='r', linewidth=2, markersize=5)
plt.title('ResNet-50 Training Loss over 25 Epochs', fontsize=14, fontweight='bold')
plt.xlabel('Epoch', fontsize=12)
plt.ylabel('Cross-Entropy Loss', fontsize=12)
plt.xticks(range(1, 26, 2))
plt.tight_layout()
plt.savefig('training_loss_graph.png', dpi=300)
print("✅ Saved training_loss_graph.png")
plt.close()