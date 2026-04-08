import torch
import torchvision.transforms as transforms
from PIL import Image
from torchvision.models import resnet50 
import torch.nn as nn
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

def get_prediction(image_path):
    try:
        model = resnet50()
        num_ftrs = model.fc.in_features
        model.fc = nn.Linear(num_ftrs, 2) 

        model_path = "ml_layer/medical_deepfake_resnet50_ULTIMATE.pth"
        model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
        model.eval()

        preprocess = transforms.Compose([
            transforms.Resize(256, interpolation=transforms.InterpolationMode.BILINEAR, antialias=True),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

        img = Image.open(image_path).convert('RGB')
        input_tensor = preprocess(img)
        input_batch = input_tensor.unsqueeze(0)

        with torch.no_grad():
            output = model(input_batch)
        
        probabilities = torch.nn.functional.softmax(output[0], dim=0)
        max_prob = torch.max(probabilities).item()
        confidence = int(max_prob * 100)
        
        predicted_class_index = torch.argmax(probabilities).item()
        verdict = "Fake" if predicted_class_index == 1 else "Real"
        
        return verdict, confidence

    except Exception as e:
        print(f"[Error] ML Layer: {e}")
        return "Error", 0