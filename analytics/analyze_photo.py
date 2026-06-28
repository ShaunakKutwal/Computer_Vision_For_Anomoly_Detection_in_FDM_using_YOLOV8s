# src/analyze_photo.py
import cv2
from ultralytics import YOLO
import sys
import os
from datetime import datetime
import glob

def analyze_photo(image_path, model_path=None, conf_threshold=0.25):
    """
    Analyze a single photo and return defect information
    """
    print("="*60)
    print("PHOTO DEFECT ANALYSIS")
    print("="*60)
    
    # Check if image exists
    if not os.path.exists(image_path):
        print(f" ERROR: Image not found at: {image_path}")
        return None
    
    # Find model if not specified
    if model_path is None:
        model_files = glob.glob('runs/**/best.pt', recursive=True)
        if not model_files:
            print(" ERROR: No model found!")
            return None
        model_path = model_files[0]
        print(f" Using model: {model_path}")
    
    # Load model
    try:
        model = YOLO(model_path)
        print(f" Model loaded successfully!")
        print(f"🔍 Detecting: {list(model.names.values())}")
    except Exception as e:
        print(f" ERROR loading model: {e}")
        return None
    
    # Read image
    img = cv2.imread(image_path)
    if img is None:
        print(f" ERROR: Could not read image")
        return None
    
    h, w = img.shape[:2]
    print(f"\n Image: {os.path.basename(image_path)}")
    print(f"   Size: {w}x{h} pixels")
    
    # Run detection
    print(f"\n Analyzing with confidence threshold: {conf_threshold}")
    results = model(image_path, conf=conf_threshold)
    
    # Process results
    defects = []
    if results[0].boxes is not None and len(results[0].boxes) > 0:
        print(f"\n DEFECTS FOUND: {len(results[0].boxes)}")
        print("-"*50)
        
        for i, box in enumerate(results[0].boxes):
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            class_name = model.names[cls_id]
            
            # Get box coordinates
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            
            # Calculate box info
            box_w = x2 - x1
            box_h = y2 - y1
            box_area = box_w * box_h
            img_area = w * h
            area_percentage = (box_area / img_area) * 100
            
            # Calculate center
            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2
            
            defect_info = {
                'index': i + 1,
                'class': class_name,
                'confidence': conf,
                'box': {
                    'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2,
                    'width': box_w, 'height': box_h
                },
                'center': {'x': center_x, 'y': center_y},
                'area': {
                    'pixels': box_area,
                    'percentage': area_percentage
                }
            }
            defects.append(defect_info)
            
            # Print detailed info
            print(f"\n Defect #{i+1}: {class_name.upper()}")
            print(f"   Confidence: {conf:.2%}")
            print(f"   Location: ({x1}, {y1}) to ({x2}, {y2})")
            print(f"   Size: {box_w} x {box_h} pixels")
            print(f"   Area: {area_percentage:.1f}% of image")
            print(f"   Center: ({center_x:.1f}, {center_y:.1f})")
    else:
        print("\n NO DEFECTS FOUND")
        print("   The image appears to be normal.")
    
    # Save annotated image
    output_path = image_path.replace('.jpg', '_analyzed.jpg')
    if not output_path.endswith('_analyzed.jpg'):
        output_path = image_path + '_analyzed.jpg'
    
    annotated = results[0].plot()
    cv2.imwrite(output_path, annotated)
    print(f"\n Annotated image saved to: {output_path}")
    
    # Summary
    print("\n" + "="*50)
    print("SUMMARY")
    print("="*50)
    print(f"Total defects: {len(defects)}")
    if defects:
        by_class = {}
        for d in defects:
            by_class[d['class']] = by_class.get(d['class'], 0) + 1
        print("By type:")
        for class_name, count in by_class.items():
            print(f"  • {class_name}: {count}")
    
    print("="*60)
    return defects

def main():
    """Main function to handle command line arguments"""
    print("\n📸 PHOTO DEFECT ANALYZER")
    print("-"*40)
    
    # Get image path from user
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        image_path = input("Enter path to image: ").strip()
    
    # Get optional confidence threshold
    if len(sys.argv) > 2:
        try:
            conf = float(sys.argv[2])
        except:
            conf = 0.25
    else:
        conf_input = input("Confidence threshold [0.25]: ").strip()
        conf = float(conf_input) if conf_input else 0.25
    
    # Analyze the photo
    defects = analyze_photo(image_path, conf_threshold=conf)
    
    # Option to save report
    if defects:
        save_report = input("\n Save detailed report to file? (y/n): ").lower()
        if save_report == 'y':
            report_name = input("Report filename [defect_report.txt]: ").strip()
            if not report_name:
                report_name = 'defect_report.txt'
            
            with open(report_name, 'w') as f:
                f.write("="*60 + "\n")
                f.write("DEFECT ANALYSIS REPORT\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Image: {os.path.basename(image_path)}\n")
                f.write("="*60 + "\n\n")
                
                for d in defects:
                    f.write(f"Defect #{d['index']}: {d['class'].upper()}\n")
                    f.write(f"  Confidence: {d['confidence']:.2%}\n")
                    f.write(f"  Location: ({d['box']['x1']}, {d['box']['y1']}) to ({d['box']['x2']}, {d['box']['y2']})\n")
                    f.write(f"  Size: {d['box']['width']}x{d['box']['height']} pixels\n")
                    f.write(f"  Area: {d['area']['percentage']:.1f}% of image\n")
                    f.write(f"  Center: ({d['center']['x']:.1f}, {d['center']['y']:.1f})\n\n")
                
                f.write("="*60 + "\n")
                f.write(f"Total defects: {len(defects)}\n")
                f.write("="*60 + "\n")
            
            print(f" Report saved to: {report_name}")

if __name__ == "__main__":
    main()