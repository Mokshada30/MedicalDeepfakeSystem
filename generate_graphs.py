import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, roc_curve, auc
from ml_layer.detector import get_prediction

# Set the path to your test data
TEST_DIR = "test_dataset"

def prep_image_for_ai(file_path):
    """Converts .npy to .png so the ResNet model can actually read it!"""
    if file_path.endswith(".npy"):
        try:
            data = np.load(file_path)
            # Normalize the numpy array to 0-255 pixel values
            data_norm = ((data - data.min()) / (data.max() - data.min()) * 255).astype(np.uint8)
            img = Image.fromarray(data_norm)
            
            # Save as PNG
            png_path = file_path.replace(".npy", ".png")
            img.save(png_path)
            
            # Delete the original .npy to keep the folder clean (optional, but helpful)
            os.remove(file_path) 
            return png_path
        except Exception as e:
            print(f"Error converting {file_path}: {e}")
            return None
    return file_path

def evaluate_model():
    y_true = []
    y_pred = []
    y_scores = [] 

    print("Evaluating Model on Test Dataset (Converting .npy files if found)...")
    
    # Process Real Images (Label = 0)
    real_dir = os.path.join(TEST_DIR, "Real")
    if os.path.exists(real_dir):
        for file in os.listdir(real_dir):
            if file.endswith(('.png', '.jpg', '.jpeg', '.npy')):
                path = os.path.join(real_dir, file)
                
                # Run the converter first!
                processing_path = prep_image_for_ai(path)
                
                if processing_path:
                    verdict, conf = get_prediction(processing_path)
                    y_true.append(0) 
                    y_pred.append(0 if verdict.lower() == 'real' else 1)
                    y_scores.append((100 - conf)/100.0 if verdict.lower() == 'fake' else conf/100.0)

    # Process Fake Images (Label = 1)
    fake_dir = os.path.join(TEST_DIR, "Fake")
    if os.path.exists(fake_dir):
        for file in os.listdir(fake_dir):
            if file.endswith(('.png', '.jpg', '.jpeg', '.npy')):
                path = os.path.join(fake_dir, file)
                
                # Run the converter first!
                processing_path = prep_image_for_ai(path)
                
                if processing_path:
                    verdict, conf = get_prediction(processing_path)
                    y_true.append(1) 
                    y_pred.append(0 if verdict.lower() == 'real' else 1)
                    y_scores.append(conf/100.0 if verdict.lower() == 'fake' else (100 - conf)/100.0)

    return y_true, y_pred, y_scores

def plot_confusion_matrix(y_true, y_pred):
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=['Real', 'Fake'], 
                yticklabels=['Real', 'Fake'],
                annot_kws={"size": 16})
    plt.title('ResNet-50 Confusion Matrix', fontsize=14, fontweight='bold')
    plt.ylabel('Actual Label', fontsize=12)
    plt.xlabel('Predicted Label', fontsize=12)
    plt.tight_layout()
    plt.savefig('confusion_matrix.png', dpi=300) 
    print("✅ Saved confusion_matrix.png")

def plot_roc_curve(y_true, y_scores):
    fpr, tpr, thresholds = roc_curve(y_true, y_scores)
    roc_auc = auc(fpr, tpr)
    
    plt.figure(figsize=(6, 5))
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate', fontsize=12)
    plt.ylabel('True Positive Rate', fontsize=12)
    plt.title('Receiver Operating Characteristic (ROC)', fontsize=14, fontweight='bold')
    plt.legend(loc="lower right")
    plt.tight_layout()
    plt.savefig('roc_curve.png', dpi=300)
    print("✅ Saved roc_curve.png")

if __name__ == "__main__":
    y_true, y_pred, y_scores = evaluate_model()
    
    if len(y_true) > 0:
        acc = accuracy_score(y_true, y_pred)
        prec = precision_score(y_true, y_pred)
        rec = recall_score(y_true, y_pred)
        
        print("\n--- RESULTS FOR RESEARCH PAPER ---")
        print(f"Accuracy:  {acc*100:.2f}%")
        print(f"Precision: {prec*100:.2f}%")
        print(f"Recall:    {rec*100:.2f}%")
        print("----------------------------------\n")
        
        plot_confusion_matrix(y_true, y_pred)
        plot_roc_curve(y_true, y_scores)
    else:
        print("Error: No images found or processed successfully in test_dataset.")