# src/load_images.py
import os
import shutil
import glob
from pathlib import Path

def load_images_from_folder():
    """
    Load JPG images from a user-specified folder into the dataset
    """
    print("="*60)
    print("IMAGE LOADER - AUTO IMPORT JPG FILES")
    print("="*60)
    
    # Get source folder path from user
    source_path = input("\n Enter the path to your image folder: ").strip()
    
    # Remove quotes if user added them
    source_path = source_path.strip('"').strip("'")
    
    # Check if source folder exists
    if not os.path.exists(source_path):
        print(f" ERROR: Folder not found: {source_path}")
        return
    
    print(f"\n Scanning folder: {source_path}")
    
    # Find all JPG images (case insensitive)
    jpg_files = []
    for ext in ['*.jpg', '*.jpeg', '*.JPG', '*.JPEG']:
        jpg_files.extend(glob.glob(os.path.join(source_path, ext)))
    
    if not jpg_files:
        print(" No JPG images found in this folder!")
        return
    
    print(f" Found {len(jpg_files)} JPG images")
    
    # Show sample of found images
    print("\n Sample images found:")
    for i, img in enumerate(jpg_files[:5]):
        print(f"   {i+1}. {os.path.basename(img)}")
    if len(jpg_files) > 5:
        print(f"   ... and {len(jpg_files)-5} more")
    
    # Ask which defect class these images belong to
    print("\n Which defect class do these images belong to?")
    print("   1. stringing")
    print("   2. cracking")
    print("   3. off_platform")
    print("   4. normal (no defects)")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    defect_map = {
        '1': 'stringing',
        '2': 'cracking', 
        '3': 'off_platform',
        '4': 'normal'
    }
    
    if choice not in defect_map:
        print(" Invalid choice!")
        return
    
    defect = defect_map[choice]
    print(f"\n Copying images to: dataset/images/{defect}/")
    
    # Create destination folder if it doesn't exist
    dest_folder = f'dataset/images/{defect}'
    os.makedirs(dest_folder, exist_ok=True)
    
    # Copy images
    copied = 0
    skipped = 0
    
    for img_path in jpg_files:
        img_name = os.path.basename(img_path)
        dest_path = os.path.join(dest_folder, img_name)
        
        # Check if file already exists
        if os.path.exists(dest_path):
            print(f"  Skipping (already exists): {img_name}")
            skipped += 1
        else:
            shutil.copy2(img_path, dest_path)
            print(f" Copied: {img_name}")
            copied += 1
    
    print("\n" + "="*60)
    print(" SUMMARY")
    print("="*60)
    print(f"Total images found: {len(jpg_files)}")
    print(f"Images copied: {copied}")
    print(f"Images skipped (already exist): {skipped}")
    print(f"Destination: dataset/images/{defect}/")
    
    # Ask if user wants to create empty label files
    if defect != 'normal':
        create_labels = input("\n  Create empty label files for these images? (y/n): ").lower()
        if create_labels == 'y':
            label_folder = f'dataset/labels/{defect}'
            os.makedirs(label_folder, exist_ok=True)
            
            label_created = 0
            for img_path in jpg_files:
                img_name = os.path.basename(img_path)
                label_name = img_name.replace('.jpg', '.txt').replace('.jpeg', '.txt')
                label_path = os.path.join(label_folder, label_name)
                
                if not os.path.exists(label_path):
                    # Create empty label file
                    with open(label_path, 'w') as f:
                        pass
                    print(f" Created label: {label_name}")
                    label_created += 1
            
            print(f"\n Created {label_created} empty label files")
    
    print("\n Done! Run 'python src/clean_split.py' to update your dataset split.")

def batch_load_multiple_folders():
    """
    Load images from multiple folders, each for a different defect
    """
    print("="*60)
    print("BATCH IMAGE LOADER - MULTIPLE FOLDERS")
    print("="*60)
    
    defects = ['stringing', 'cracking', 'off_platform', 'normal']
    
    for defect in defects:
        print(f"\n Processing {defect.upper()} images...")
        folder = input(f"Enter path to {defect} images folder (or press Enter to skip): ").strip()
        
        if not folder:
            print(f"  Skipping {defect}")
            continue
        
        # Remove quotes
        folder = folder.strip('"').strip("'")
        
        if not os.path.exists(folder):
            print(f"   Folder not found: {folder}")
            continue
        
        # Find JPG images
        jpg_files = []
        for ext in ['*.jpg', '*.jpeg', '*.JPG', '*.JPEG']:
            jpg_files.extend(glob.glob(os.path.join(folder, ext)))
        
        if not jpg_files:
            print(f"   No JPG images found in {folder}")
            continue
        
        print(f"   Found {len(jpg_files)} images")
        
        # Copy images
        dest_folder = f'dataset/images/{defect}'
        os.makedirs(dest_folder, exist_ok=True)
        
        copied = 0
        for img_path in jpg_files:
            img_name = os.path.basename(img_path)
            dest_path = os.path.join(dest_folder, img_name)
            
            if not os.path.exists(dest_path):
                shutil.copy2(img_path, dest_path)
                copied += 1
                print(f"    Copied: {img_name}")
        
        print(f"   Copied {copied} images to {dest_folder}")
        
        # Create empty labels for non-normal defects
        if defect != 'normal':
            create_labels = input(f"  Create empty label files for {defect}? (y/n): ").lower()
            if create_labels == 'y':
                label_folder = f'dataset/labels/{defect}'
                os.makedirs(label_folder, exist_ok=True)
                
                label_count = 0
                for img_path in jpg_files:
                    img_name = os.path.basename(img_path)
                    label_name = img_name.replace('.jpg', '.txt').replace('.jpeg', '.txt')
                    label_path = os.path.join(label_folder, label_name)
                    
                    if not os.path.exists(label_path):
                        with open(label_path, 'w') as f:
                            pass
                        label_count += 1
                
                print(f"    Created {label_count} empty label files")
    
    print("\n" + "="*60)
    print(" BATCH LOAD COMPLETE")
    print("="*60)
    print("\nNext steps:")
    print("1. Run 'python src/clean_split.py' to update your dataset split")
    print("2. Train your model with 'python src/train.py'")

if __name__ == "__main__":
    print("\n IMAGE LOADER MENU")
    print("1. Load images from a single folder")
    print("2. Batch load from multiple folders (one per defect)")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice == '2':
        batch_load_multiple_folders()
    else:
        load_images_from_folder()