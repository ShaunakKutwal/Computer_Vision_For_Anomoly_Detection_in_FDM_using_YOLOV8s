# src/predict.py
from ultralytics import YOLO
import cv2
import os
import sys

def get_model_path():
    """Dynamically get the path to the trained model."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, 'models', 'best.pt')

def main():
    print("="*60)
    print("FDM ANOMALY PREDICTION TOOL - INTERACTIVE MODE")
    print("="*60)

    # 1. Locate the model
    model_path = get_model_path()
    if not os.path.exists(model_path):
        print(f"ERROR: Model not found at: {model_path}")
        print("Please ensure 'best.pt' is in the 'models' folder.")
        sys.exit(1)

    # 2. Interactive Menu
    print("\nWhat would you like to process?")
    print("  1. Single Image")
    print("  2. Video")
    print("  3. Folder of Images (Batch Processing)")
    
    choice = input("\nEnter your choice (1, 2, or 3): ").strip()

    if choice not in ['1', '2', '3']:
        print("Invalid choice. Exiting.")
        sys.exit(1)

    # 3. Get the file/folder path
    print("\n(Tip: You can just drag and drop the file directly into this terminal!)")
    source_path = input("Enter the path: ").strip()
    
    # Strip quotes in case the user dragged and dropped the file in Windows
    source_path = source_path.strip('"\'')

    if not os.path.exists(source_path):
        print(f"\nERROR: Could not find anything at: {source_path}")
        sys.exit(1)

    # 4. Load the model
    print(f"\nLoading model...")
    model = YOLO(model_path)
    conf_threshold = 0.25
    print("Model loaded successfully!\n")

    # 5. Process based on choice
    if choice == '1':
        print(f"Analyzing Image: {os.path.basename(source_path)}")
        results = model(source_path, conf=conf_threshold)
        result = results[0]
        
        output_path = f"predicted_{os.path.basename(source_path)}"
        
        if result.boxes is not None and len(result.boxes) > 0:
            annotated = result.plot()
            cv2.imwrite(output_path, annotated)
            print(f"\nSUCCESS! Saved annotated image to: {output_path}")
            print("\nDETECTIONS FOUND:")
            print("-" * 30)
            for i, box in enumerate(result.boxes):
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                class_name = model.names[cls_id]
                print(f"{i+1}. {class_name} (Confidence: {conf:.2%})")
        else:
            print("\nNo defects detected in this image.")

    elif choice == '2':
        print(f"Analyzing Video: {os.path.basename(source_path)}")
        print("Please wait, this may take a few moments depending on video length...")
        
        output_dir = os.path.join(os.path.dirname(model_path), '..', 'alerts', 'video_predictions')
        os.makedirs(output_dir, exist_ok=True)
        
        # YOLO native video processing
        model.predict(source=source_path, conf=conf_threshold, save=True, project=output_dir, name="processed", exist_ok=True)
        
        print(f"\nSUCCESS! Video processing complete.")
        print(f"Your video was saved to: {os.path.join(output_dir, 'processed')}")

    elif choice == '3':
        print(f"Analyzing Folder: {os.path.basename(source_path)}")
        output_dir = source_path + "_predictions"
        os.makedirs(output_dir, exist_ok=True)
        
        images = [f for f in os.listdir(source_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        if not images:
            print("No valid images found in that folder.")
            sys.exit(1)
            
        defect_count = 0
        
        for i, img_name in enumerate(images):
            img_path = os.path.join(source_path, img_name)
            results = model(img_path, conf=conf_threshold, verbose=False)
            result = results[0]
            
            annotated = result.plot()
            cv2.imwrite(os.path.join(output_dir, f"pred_{img_name}"), annotated)
            
            if result.boxes is not None and len(result.boxes) > 0:
                defect_count += len(result.boxes)
                print(f"[{i+1}/{len(images)}] {img_name}: Found {len(result.boxes)} defect(s)!")
            else:
                print(f"[{i+1}/{len(images)}] {img_name}: Clear")
                
        print("\n" + "="*50)
        print(f"Batch processing complete!")
        print(f"Total defects found across all images: {defect_count}")
        print(f"Results saved to: {output_dir}")

if __name__ == "__main__":
    main()