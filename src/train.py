import os
import shutil
import torch
from ultralytics import YOLO

def main():
    print("="*50)
    print("STARTING TRAINING - 3 DEFECTS: stringing, cracking, off_platform")
    print("="*50)
    
    # Get absolute paths to avoid terminal working directory issues
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    data_yaml_path = os.path.join(project_root, 'data.yaml')
    models_dir = os.path.join(project_root, 'models')
    runs_dir = os.path.join(project_root, 'runs', 'train')
    
    # Ensure the models directory exists
    os.makedirs(models_dir, exist_ok=True)

    # Check if GPU is available
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Using device: {device}")
    
    # Load YOLOv8s base model (Change to os.path.join(models_dir, 'best.pt') if fine-tuning)
    print("Loading YOLOv8s model...")
    model = YOLO('yolov8s.pt')
    
    # Start training
    print(f"Using data config: {data_yaml_path}")
    print("Beginning training with data augmentation...")
    print("This may take several hours. Please be patient.")
    print("="*50)
    
    # Run training
    results = model.train(
        data=data_yaml_path,
        epochs=150,
        imgsz=768,
        batch=16,
        device=device,
        patience=20,
        save=True,
        project=runs_dir,
        name='training_session',
        exist_ok=True,
        pretrained=True,
        
        # Data augmentation parameters
        hsv_h=0.015,
        hsv_s=0.7,
        hsv_v=0.4,
        degrees=10.0,
        translate=0.1,
        scale=0.5,
        shear=2.0,
        perspective=0.0001,
        flipud=0.0,
        fliplr=0.5,
        mosaic=1.0,
        mixup=0.2,
        copy_paste=0.1,
        augment=True,
        
        verbose=True
    )
    
    print("="*50)
    print("TRAINING PROCESS COMPLETED!")
    print("="*50)

    # Post-Training Automation: Copy the best model to the root 'models' folder
    trained_weights_path = os.path.join(runs_dir, 'training_session', 'weights', 'best.pt')
    final_model_dest = os.path.join(models_dir, 'best.pt')

    if os.path.exists(trained_weights_path):
        shutil.copy(trained_weights_path, final_model_dest)
        print(f"SUCCESS: Auto-copied new weights to {final_model_dest}")
        print("Your IoT pipeline is ready to use the updated model.")
    else:
        print(f"WARNING: Could not find trained weights at {trained_weights_path}")

if __name__ == '__main__':
    # This ensures multiprocessing works correctly on Windows
    from multiprocessing import freeze_support
    freeze_support()
    main()