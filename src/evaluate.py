# src/evaluate.py
from ultralytics import YOLO
import yaml
import os
import matplotlib.pyplot as plt
import numpy as np

def evaluate_model(model_path=None, data_yaml='data.yaml'):
    """
    Evaluate model performance on validation set
    """
    print("="*50)
    print("MODEL EVALUATION")
    print("="*50)
    
    # Get absolute paths to avoid terminal working directory issues
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir) # Goes up one level from 'src'
    
    # Fix data_yaml path if it's just the default string
    if data_yaml == 'data.yaml':
        data_yaml = os.path.join(project_root, 'data.yaml')
    
    # Find model automatically if not specified
    if model_path is None:
        import glob
        # Search in the root/models directory
        search_pattern = os.path.join(project_root, 'models', '**', 'best.pt')
        model_files = glob.glob(search_pattern, recursive=True)
        
        if model_files:
            model_path = model_files[0]
            print(f"Found model at: {model_path}")
        else:
            print("ERROR: No trained model found!")
            return
    
    # Check if model exists
    if not os.path.exists(model_path):
        print(f"ERROR: Model not found at {model_path}")
        return
    
    if not os.path.exists(data_yaml):
        print(f"ERROR: Data config not found at {data_yaml}")
        return

    # Load model
    print(f"Loading model: {model_path}")
    model = YOLO(model_path)
    
    # Load data config
    with open(data_yaml, 'r') as f:
        data = yaml.safe_load(f)
    
    class_names = data['names']
    print(f"Classes: {class_names}")
    
    # Run validation
    print("\nRunning validation on test set...")
    metrics = model.val(
        data=data_yaml,
        split='test',
        conf=0.25,
        iou=0.45,
        batch=16,
        plots=True
    )
    
    # Print overall metrics
    print("\n" + "="*50)
    print("OVERALL METRICS")
    print("="*50)
    print(f"mAP50: {metrics.box.map50:.4f}")
    print(f"mAP50-95: {metrics.box.map:.4f}")
    print(f"Precision: {metrics.box.mp:.4f}")
    print(f"Recall: {metrics.box.mr:.4f}")
    print(f"F1-score: {2 * (metrics.box.mp * metrics.box.mr) / (metrics.box.mp + metrics.box.mr + 1e-16):.4f}")
    
    # Per-class metrics using correct attribute names
    print("\n" + "="*50)
    print("PER-CLASS METRICS")
    print("="*50)
    
    print(f"{'Class':<20} {'Precision':<12} {'Recall':<12} {'mAP50':<12} {'mAP50-95':<12}")
    print("-"*68)
    
    for i, name in enumerate(class_names):
        if i < len(metrics.box.ap_class_index):
            p = metrics.box.p[i] if i < len(metrics.box.p) else 0
            r = metrics.box.r[i] if i < len(metrics.box.r) else 0
            ap50 = metrics.box.ap50[i] if i < len(metrics.box.ap50) else 0
            ap = metrics.box.ap[i] if i < len(metrics.box.ap) else 0
            print(f"{name:<20} {p:<12.4f} {r:<12.4f} {ap50:<12.4f} {ap:<12.4f}")
        else:
            print(f"{name:<20} {'N/A':<12} {'N/A':<12} {'N/A':<12} {'N/A':<12}")
    
    print("\n" + "="*50)
    print("EVALUATION COMPLETE")
    print("="*50)
    print(f"\nDetailed plots saved in: {metrics.save_dir}")
    
    return metrics

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Evaluate 3D print defect detection model')
    parser.add_argument('--model', type=str, default=None,
                        help='Path to trained model (auto-detected if not specified)')
    parser.add_argument('--data', type=str, default='data.yaml',
                        help='Path to data.yaml file')
    
    args = parser.parse_args()
    evaluate_model(args.model, args.data)